/**************************************************************
**            3D First Break Traveltime Tomography           **
**                         =============                     **
**                         Ding Pengcheng                    **
**                             2015.08                       **
**  Copyright (c) China University of Petroleum (East China) **
**                        QingDao, China, 2015               **
**                      All rights reserved.                 **
**  WARNING:                                                 **
**              THE ONLY PURPOSE OF THIS PROGRAM             **
**                            IS TO                          **
**                HOOYOU TARIUM OILFIELD COMPANY             **
**               NO WARRANTY FOR THE GOOD RESULTS!           **
**************************************************************/	
#include "rsf.h"
#include <stdio.h>
#include <malloc.h>
#include "fastmarchvti.h"
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
#include <mpi.h>
#include <omp.h>

int *readpar(int *nshot,int *nray,int *nx,int *ny,int *nz,float *dx,float *dy,float *dz,float *v0,float *dv,float *delta,int *sign,float *damp,float *lamda,float *sz,float *omega,int *itmax,int *niter,char *cele,char *cshot,char *crec,char *ccount);
void buildtomo(float *vel,float *vx,float *q,float ***eps,float ***deta,float ***vel3D,float ***vel_x3D,float ***vel_q3D,int nx,int ny,int nz,float dx,float dy,float dz,float v0,float dv,int nshot,int nray,char *cele,char *cshot,char *crec,char *ccount,float **ele,float **shotxyz,float **recxyz,int *neachshot,float *eps1,float *deta1);
void buildtomo1(float *realvel,float *realvx,float *realq,float ***realeps,float ***realdeta,float ***realvel3D,int nx,int ny,int nz,float dx,float dy,float dz,float v0,float dv,int nshot,int nray,char *cele,char *cshot,char *crec,char *ccount,float **ele,float **shotxyz,float **recxyz,int *neachshot);
void  RegLSQR(int nrays,int nmax,int nraysapp,int nmaxapp,int sign,int nx,int ny,int nz,float damp,float lamda,float sz,float omega,int itmax,int layer_cell_num,float *deltat,int *frenum,float *frelen,float *ds,float ***sel3D,float *deltatapp,int *frenumapp,float *frelenapp,float ***dens); 
void vsm3d(float ***vel,int n3,int n2,int n1,int iter,int depth,float r3,float r2,float r1,float mu,int sl,float vminc,float vmaxc);
int sum(int *neachshot,int is); 
bool RK4STEP_3D(float *gradientArray, int *gradientArraySize, float *startPoint, float *nextPoint, float stepSize,float dx,float dy,float dz);
void rk4(float *StartPoint,float *gradientArray,float Stepsize,int nx,int ny,int nz,float dx,float dy,float dz,float *nexpoint);
int shortestpath(float ***time,float *StartPoint,float *SourcePoint,float Stepsize,float *gradientArray,int nx,int ny,int nz,float dx,float dy,float dz,FILE *frechet,FILE *fdelta,int *nmax,int *countdt,FILE *fp1,FILE *fp2,FILE *fp3,int myid,int numprocs,float dt,int *gArraym,float *freArraym,float *freArraym_x,float *freArraym_z,float *freArraym_e,int *calm,float *eps1,float *deta1,float *vel);
void laplace(float ***time,int nx,int ny,int nz,float dx,float dy,float dz,float ***gx,float ***gy,float ***gz);
void interpgrad3d(float *Ireturn,float *Grad,int *Isize, float *point,float dx,float dy,float dz);
float norm3(float *a);
int checkBounds3d( float *point, int *Isize,float dx,float dy,float dz) ;
int mindex3(int x, int y, int z, int sizx, int sizy);
void smooth(float ***vel3D,float *ds,int nx,int ny,int nz);
void smooth3(float ***vel3D,float ***vel_x3D,float ***vel_q3D,float ***eps,float ***deta,int nx,int ny,int nz);
void appvel(int nx,int ny,int nz,int js,float **recxyz,FILE *frechetapp,FILE *fdeltaapp,int *nmaxapp,int *countdtapp,float dt1,float dt2,int *gArray1,float *freArray1,int cal1,int *gArray2,float *freArray2,int cal2);

int main(int argc,char *argv[])
{
	int myid,numprocs;
	int i,j,k,is,js,nshot,caltr=0,nray=0,count=0,nmax=0,nmaxapp=0,sign,itmax,niter=1,iter,countdt=0,countdtapp=0,siren1=0,siren2=0,ifree;
	int *tempnmax,*tempcountdt,*tempnmaxapp,*tempcountdtapp,sumnmax,sumcountdt,sumnmaxapp,sumcountdtapp;
	int nx,ny,nz,*flag,*neachshot,*frenum,*sfrenum,*sfrenumapp;
	float dx,dy,dz,v0,dv,damp,lamda,sz,omega,*frelen,*sfrelen,*sfrelen_x,*sfrelen_z,*sfrelen_e,*sfrelenapp,*deltat,*sdeltat,*sdeltatapp,*ds,*ds_x,*ds_e,sumdelta=0,dt=0,delta,dt1,dt2,initdelta=0;
	float ***dens;
	float shotpoint[3],recpoint[3];
	float *vel,*time,**ele,**shotxyz,**recxyz,*t0,*q,*time1,*time2,*vx,*realvel,*realvx,*realq,*deta1,*eps1;
	float ***eps,***deta,***vel3D,***time3D,***sel3D,***vel_x3D,***vel_q3D,*realtimefb;
      float ***realeps,***realdeta,***realvel3D,***realtime3Dfb;
	float r1=50,r2=50,r3=25,vminc=340,vmaxc=2000;
	float ***gx,***gy,***gz,*gradientArray;
	float *freArray1_x,*freArray2_x,*freArray1_z,*freArray2_z,*freArray1_e,*freArray2_e;
      float *freArray1,*freArray2;
	int *gArray1,*gArray2,cal1=0,cal2=0;
	bool plane[3];
	char cele[50],cshot[50],crec[50],ccount[50];
	char FN1[50]={"grid_x.txt"},FN2[50]={"grid_y.txt"},FN3[50]={"grid_z.txt"},FNfre[50]="",FNdt[50]="",FNfreapp[50]="",FNdtapp[50]="",FRECHET[50]={"frechet.txt"},FDELTA[50]={"fdelta.txt"},FRECHETAPP[50]={"frechetapp.txt"},FDELTAAPP[50]={"fdeltaapp.txt"};
	
 	FILE *frechet,*fb,*velupdate,*epsupdate,*detaupdate,*fdelta,*frechetapp,*fdeltaapp,*fdensity;
	FILE *fp1,*fp2,*fp3,*fprealvel,*fprealeps,*fprealdeta,*fpvinitial,*fpepsinitial,*fpdetainitial;
      MPI_Status status;
 
	fb=fopen("fb.txt","r");
	fdensity=fopen("density.dat","wb");  
	for(i=0;i<3;i++)plane[i]=false;
	/* read par file */   
	neachshot=readpar(&nshot,&nray,&nx,&ny,&nz,&dx,&dy,&dz,&v0,&dv,&delta,&sign,&damp,&lamda,&sz,&omega,&itmax,&niter,cele,cshot,crec,ccount);
	t0=sf_floatalloc(nray);
	/* ifree is the maximum ray path length */
	ifree=(int)(2*sqrt((nx*dx)*(nx*dx)+(ny*dy)*(ny*dy)+(nz*dz)*(nz*dz))/delta);
	/* read the first break file */
	//for(i=0;i<nray;i++)fscanf(fb,"%f\n",&t0[i]);
	//fclose(fb);
       // initial velmodel allocate size
	vel=sf_floatalloc(nz*ny*nx);
	time=sf_floatalloc(nz*ny*nx);
      time1=sf_floatalloc(nz*ny*nx);
      time2=sf_floatalloc(nz*ny*nx);
      vx=sf_floatalloc(nz*ny*nx);
      q=sf_floatalloc(nz*ny*nx);
      deta1=sf_floatalloc(nz*ny*nx);
      eps1=sf_floatalloc(nz*ny*nx);
	flag=sf_intalloc(nz*ny*nx);
	vel3D=sf_floatalloc3(nz,ny,nx);
      vel_x3D=sf_floatalloc3(nz,ny,nx);
      vel_q3D=sf_floatalloc3(nz,ny,nx);
	sel3D=sf_floatalloc3(nz,ny,nx);
      eps=sf_floatalloc3(nz,ny,nx);
      deta=sf_floatalloc3(nz,ny,nx);
	time3D=sf_floatalloc3(nz,ny,nx);
       //real velmodel allocate size
	realvel=sf_floatalloc(nz*ny*nx);
	realtimefb=sf_floatalloc(nz*ny*nx);
      realvx=sf_floatalloc(nz*ny*nx);
      realq=sf_floatalloc(nz*ny*nx);
	realvel3D=sf_floatalloc3(nz,ny,nx);
	realeps=sf_floatalloc3(nz,ny,nx);
      realdeta=sf_floatalloc3(nz,ny,nx);
	realtime3Dfb=sf_floatalloc3(nz,ny,nx);
	ele=sf_floatalloc2(ny,nx);
	shotxyz=sf_floatalloc2(3,nshot);
	recxyz=sf_floatalloc2(3,nray);
      //LSQR parameter set
	deltat=sf_floatalloc(nray);
	ds=sf_floatalloc(nx*ny*nz);
	ds_x=sf_floatalloc(nx*ny*nz);
	ds_e=sf_floatalloc(nx*ny*nz);
	gArray1=sf_intalloc(ifree);
	gArray2=sf_intalloc(ifree);
	freArray1=sf_floatalloc(ifree);
	freArray2=sf_floatalloc(ifree);
	freArray1_x=sf_floatalloc(ifree);
	freArray2_x=sf_floatalloc(ifree);
	freArray1_z=sf_floatalloc(ifree);
	freArray2_z=sf_floatalloc(ifree);
	freArray1_e=sf_floatalloc(ifree);
	freArray2_e=sf_floatalloc(ifree);

	gx=sf_floatalloc3(nz,ny,nx);
	gy=sf_floatalloc3(nz,ny,nx);
	gz=sf_floatalloc3(nz,ny,nx);
	gradientArray=sf_floatalloc(3*nz*ny*nx);
	dens=sf_floatalloc3(nz,ny,nx);

       fprealvel=fopen("realvel.dat","wb+"); fprealeps=fopen("realvx_bp.dat","wb+"); fprealdeta=fopen("realeta_bp.dat","wb+");
          fpvinitial=fopen("vinitial.dat","wb+"); fpepsinitial=fopen("epsinitial.dat","wb+"); fpdetainitial=fopen("detainitial.dat","wb+");
      /*build real velocity and shot,rec,count for tomo */
	buildtomo1(realvel,realvx,realq,realeps,realdeta,realvel3D,nx,ny,nz,dx,dy,dz,v0,dv,nshot,nray,cele,cshot,crec,ccount,ele,shotxyz,recxyz,neachshot);


      /*build initial velocity and shot,rec,count for tomo */
	buildtomo(vel,vx,q,eps,deta,vel3D,vel_x3D,vel_q3D,nx,ny,nz,dx,dy,dz,v0,dv,nshot,nray,cele,cshot,crec,ccount,ele,shotxyz,recxyz,neachshot,eps1,deta1);

  	/*for(i=0;i<nx;i++)
		for(j=0;j<ny;j++)
			for(k=0;k<nz;k++)
				{
                           fwrite(&vel3D[i][j][k],sizeof(float),1,fpvinitial); 
                           fwrite(&eps[i][j][k],sizeof(float),1,fpepsinitial); 
                           fwrite(&deta[i][j][k],sizeof(float),1,fpdetainitial); 
                                 }
         fclose(fpvinitial); fclose(fpepsinitial);fclose(fpdetainitial);*/
           
	MPI_Init(&argc,&argv);
	MPI_Comm_rank( MPI_COMM_WORLD, &myid);
	MPI_Comm_size( MPI_COMM_WORLD, &numprocs);
	MPI_Barrier(MPI_COMM_WORLD); 

	tempnmax=sf_intalloc(numprocs);
	tempcountdt=sf_intalloc(numprocs);
	tempnmaxapp=sf_intalloc(numprocs);
	tempcountdtapp=sf_intalloc(numprocs);

	if(myid==0){printf("==========The 3D VTI First Break Tomo Start==========\n");}
	/* traveltime calculation and ray tracing based on second order fast marching method */
	/*for(is=0+myid;is<nshot;is=is+myid)
		{
			fastmarch_init(nx,ny,nz);
			fastmarch(realtimefb,time1,realvx,realvel,realq,flag,plane,nx,ny,nz,0,0,0,dx,dy,dz,shotxyz[is][0],shotxyz[is][1],shotxyz[is][2],1,1,1,1);
			fastmarch_close();
			printf("Realmodel VTIMSFMM of %d shot has been calculated\n",is+1);
			count=0;
			for(i=0;i<nx;i++)
				for(j=0;j<ny;j++)
					for(k=0;k<nz;k++)
					{
						realtime3Dfb[is][i][j][k]=realtimefb[count];
						count++;

					}
                     //  printf("realtime=%f\n",realtime3Dfb[is][(int)(recxyz[is][0]/dx)][(int)(recxyz[is][1]/dy)][(int)(recxyz[is][2]/dz)]);
              }*/

	for(iter=0;iter<niter;iter++)
	{
	/* read the updated velocity for the iteration 2,3,4.. */
		if(iter>0)
		{
			velupdate=fopen("velupdate.dat","rb");
			epsupdate=fopen("epsupdate.dat","rb");
			detaupdate=fopen("detaupdate.dat","rb");
			count=0;
			for(i=0;i<nx;i++)		
				for(j=0;j<ny;j++)
					for(k=0;k<nz;k++){
						fread(&vel3D[i][j][k],4,1,velupdate);
                                    fread(&eps[i][j][k],4,1,epsupdate);
                                    fread(&deta[i][j][k],4,1,detaupdate);
			 			vel[count]=(1/vel3D[i][j][k])*(1/vel3D[i][j][k]);
                                   // vel_x3D[i][j][k]=vel3D[i][j][k]*sqrt(1+2*eps[i][j][k]);
                                 //   eps1[count]=eps[i][j][k];
                                  //  deta1[count]=deta[i][j][k];
                                    q[count]=(1+2*deta[i][j][k])/(1+2*eps[i][j][k]);
                                    vx[count]=vel[count]/(1+2*eps[i][j][k]);       
		        	            count++;
			 			}
		fclose(velupdate);fclose(epsupdate);fclose(detaupdate);
		}
 
		if(myid==0){printf("***************THE %d ITERATION***************\n",iter+1);}
		sprintf(FNfre,"frechet%d.dat",myid);
		sprintf(FNdt,"fdelta%d.dat",myid);
		sprintf(FNfreapp,"frechetapp%d.dat",myid);
		sprintf(FNdtapp,"fdeltaapp%d.dat",myid);

		frechet=fopen(FNfre,"wb");
		fdelta=fopen(FNdt,"wb");
  		frechetapp=fopen(FNfreapp,"wb");
  		fdeltaapp=fopen(FNdtapp,"wb");
   		sumdelta=0;
   		countdt=0;nmax=0;sumnmax=0;sumcountdt=0;
		countdtapp=0;nmaxapp=0;sumnmaxapp=0;sumcountdtapp=0;
	/* open the ray path file (only for monitor purpose) */
// 		if(myid==0){fp1=fopen(FN1,"w");fp2=fopen(FN2,"w");fp3=fopen(FN3,"w");}


		for(is=0+myid;is<nshot;is=is+numprocs)
		{
			fastmarch_init(nx,ny,nz);
			fastmarch(time,time2,vx,vel,q,flag,plane,nx,ny,nz,0,0,0,dx,dy,dz,shotxyz[is][0],shotxyz[is][1],shotxyz[is][2],1,1,1,1);
			fastmarch(realtimefb,time1,realvx,realvel,realq,flag,plane,nx,ny,nz,0,0,0,dx,dy,dz,shotxyz[is][0],shotxyz[is][1],shotxyz[is][2],1,1,1,1);
			fastmarch_close();
			printf("VTIMSFMM of %d shot has been calculated(ID:%d,Ite:%d)\n",is+1,myid+1,iter+1);
			count=0;
			for(i=0;i<nx;i++)
				for(j=0;j<ny;j++)
					for(k=0;k<nz;k++)
					{
						time3D[i][j][k]=time[count];
                                    realtime3Dfb[i][j][k]=realtimefb[count];
						count++;
					}

			cal1=0;cal2=0;
			for(i=0;i<ifree;i++)
			{gArray1[i]=0;gArray2[i]=0;freArray1[i]=0;freArray2[i]=0;freArray1_x[i]=0;freArray2_x[i]=0;freArray1_z[i]=0;freArray2_z[i]=0;freArray1_e[i]=0;freArray2_e[i]=0;}

			laplace(time3D,nx,ny,nz,dx,dy,dz,gx,gy,gz);
			count=0;
	 		 for(k=0;k<nz;k++)
				 for(j=0;j<ny;j++)
					 for(i=0;i<nx;i++)
						gradientArray[count++]=gx[i][j][k];
	
		 	for(k=0;k<nz;k++)
				 for(j=0;j<ny;j++)
					 for(i=0;i<nx;i++)
						gradientArray[count++]=gy[i][j][k];

			 for(k=0;k<nz;k++)
			 	for(j=0;j<ny;j++)
				 	for(i=0;i<nx;i++)
						gradientArray[count++]=gz[i][j][k];

			js=sum(neachshot,is);
                //  dt=(t0[js]-time3D[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)])*0.1;
                 // dt=realtimefb[js]-time3D[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)];
 			 dt=realtime3Dfb[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)]-time3D[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)];
                  dt1=dt;
              //   printf("%f %f %f\n",dt,realtime3Dfb[js][(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)],time3D[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)]);
			shotpoint[0]=shotxyz[is][0]+dx;shotpoint[1]=shotxyz[is][1]+dy;shotpoint[2]=shotxyz[is][2]+dz;
			recpoint[0]=recxyz[js][0]+dx;recpoint[1]=recxyz[js][1]+dy;recpoint[2]=recxyz[js][2]+dz*(1+0.1);
		siren1=shortestpath(time3D,recpoint,shotpoint,delta,gradientArray,nx,ny,nz,dx,dy,dz,frechet,fdelta,&nmax,&countdt,fp1,fp2,fp3,myid,numprocs,dt,gArray1,freArray1,freArray1_x,freArray1_z,freArray1_e,&cal1,eps1,deta1,vel);

			for(js=sum(neachshot,is)+1;js<sum(neachshot,is)+neachshot[is];js++)
			{
				//dt=(t0[js]-time3D[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)])*0.1;
                        //dt=realtimefb[js]-time3D[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)];
                        dt=realtime3Dfb[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)]-time3D[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)];
                         dt2=dt;
              //    printf("2 %f %f %f\n",dt,realtime3Dfb[is][(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)],time3D[(int)(recxyz[js][0]/dx)][(int)(recxyz[js][1]/dy)][(int)(recxyz[js][2]/dz)]);
				shotpoint[0]=shotxyz[is][0]+dx;shotpoint[1]=shotxyz[is][1]+dy;shotpoint[2]=shotxyz[is][2]+dz;
				recpoint[0]=recxyz[js][0]+dx;recpoint[1]=recxyz[js][1]+dy;recpoint[2]=recxyz[js][2]+dz*(1+0.1);

		siren2=shortestpath(time3D,recpoint,shotpoint,delta,gradientArray,nx,ny,nz,dx,dy,dz,frechet,fdelta,&nmax,&countdt,fp1,fp2,fp3,myid,numprocs,dt,gArray2,freArray2,freArray2_x,freArray2_z,freArray2_e,&cal2,eps1,deta1,vel);
		
				if(siren1==1&&siren2==1){appvel(nx,ny,nz,js,recxyz,frechetapp,fdeltaapp,&nmaxapp,&countdtapp,dt1,dt2,gArray1,freArray1,cal1,gArray2,freArray2,cal2);}

				for(i=0;i<ifree;i++)
					{gArray1[i]=0;gArray1[i]=gArray2[i];gArray2[i]=0;
					freArray1[i]=0;freArray1[i]=freArray2[i];freArray2[i]=0;}
					cal1=cal2;siren1=siren2;dt1=dt2; 
			}
   			printf("Raytrace of %d shot has been calculated(ID:%d,Ite:%d)\n",is+1,myid+1,iter+1);
		}

//		if(myid==0){fclose(fp1);fclose(fp2);fclose(fp3);}
		fclose(fdelta);fclose(frechet);fclose(fdeltaapp);fclose(frechetapp);

	/* send the information of all raypath to the 0 procs */
		if(myid!=0)
		{  
			MPI_Send(&nmax,1,MPI_INT,0,1,MPI_COMM_WORLD);
			MPI_Send(&countdt,1,MPI_INT,0,2,MPI_COMM_WORLD);
			MPI_Send(&nmaxapp,1,MPI_INT,0,3,MPI_COMM_WORLD);
			MPI_Send(&countdtapp,1,MPI_INT,0,4,MPI_COMM_WORLD);
		}

	/* only use the 0 procs to implement a LSQR inversion */
		if(myid==0)
		{
			tempnmax[0]=nmax;tempcountdt[0]=countdt;tempnmaxapp[0]=nmaxapp;tempcountdtapp[0]=countdtapp;
			for(i=1;i<numprocs;i++)
			{
				MPI_Recv(&tempnmax[i],1,MPI_INT,i,1,MPI_COMM_WORLD,&status);
				MPI_Recv(&tempcountdt[i],1,MPI_INT,i,2,MPI_COMM_WORLD,&status);
				MPI_Recv(&tempnmaxapp[i],1,MPI_INT,i,3,MPI_COMM_WORLD,&status);
				MPI_Recv(&tempcountdtapp[i],1,MPI_INT,i,4,MPI_COMM_WORLD,&status);
			}
			for(i=0;i<numprocs;i++){sumnmax=sumnmax+tempnmax[i];sumnmaxapp=sumnmaxapp+tempnmaxapp[i];}
			for(i=0;i<numprocs;i++){sumcountdt=sumcountdt+tempcountdt[i];sumcountdtapp=sumcountdtapp+tempcountdtapp[i];}
			sfrenum=sf_intalloc(sumnmax+sumcountdt);
                  sfrelen=sf_floatalloc(sumnmax+sumcountdt);
			sfrelen_x=sf_floatalloc(sumnmax+sumcountdt);
                  sfrelen_z=sf_floatalloc(sumnmax+sumcountdt);
                  sfrelen_e=sf_floatalloc(sumnmax+sumcountdt);
			sdeltat=sf_floatalloc(sumcountdt);
			sfrenumapp=sf_intalloc(sumnmaxapp+sumcountdtapp);
			sfrelenapp=sf_floatalloc(sumnmaxapp+sumcountdtapp);
			sdeltatapp=sf_floatalloc(sumcountdtapp);
	/* read the information of all raypath in the 0 procs */
			for(i=0;i<numprocs;i++)
			{
				sprintf(FNfre,"frechet%d.dat",i);
				sprintf(FNdt,"fdelta%d.dat",i);
				sprintf(FNfreapp,"frechetapp%d.dat",i);
				sprintf(FNdtapp,"fdeltaapp%d.dat",i);
				frechet=fopen(FNfre,"rb");frechetapp=fopen(FNfreapp,"rb");
				fdelta=fopen(FNdt,"rb");fdeltaapp=fopen(FNdtapp,"rb");
				for(j=sum(tempnmax,i)+sum(tempcountdt,i);j<sum(tempnmax,i+1)+sum(tempcountdt,i+1);j++)
					{
                              fread(&sfrenum[j],sizeof(int),1,frechet);
					fread(&sfrelen[j],sizeof(float),1,frechet);}
				//	fscanf(frechet,"%d %f %f %f %f\n",&sfrenum[j],&sfrelen[j],&sfrelen_x[j],&sfrelen_z[j],&sfrelen_e[j]);}
                         //    printf("%d %f %f %f %f\n",sfrenum[j],sfrelen[j],sfrelen_x[j],sfrelen_z[j],sfrelen_e[j]);}
				for(j=sum(tempcountdt,i);j<sum(tempcountdt,i+1);j++)
					fread(&sdeltat[j],sizeof(float),1,fdelta);
//					fscanf(fdelta,"%f\n",&sdeltat[j]);	
				for(j=sum(tempnmaxapp,i)+sum(tempcountdtapp,i);j<sum(tempnmaxapp,i+1)+sum(tempcountdtapp,i+1);j++)
					{
                              fread(&sfrenumapp[j],sizeof(int),1,frechetapp);
					fread(&sfrelenapp[j],sizeof(float),1,frechetapp);}
		//			fscanf(frechetapp,"%d %f %f %f\n",&sfrenumapp[j],&sfrelenapp_x[j],&sfrelenapp_z[j],&sfrelenapp_e[j]);}
  				for(j=sum(tempcountdtapp,i);j<sum(tempcountdtapp,i+1);j++)
					fread(&sdeltatapp[j],sizeof(float),1,fdeltaapp);
//					fscanf(fdeltaapp,"%f\n",&sdeltatapp[j]);	
				fclose(frechet);fclose(fdelta);fclose(frechetapp);fclose(fdeltaapp);
				remove(FNfre);remove(FNdt);remove(FNfreapp);remove(FNdtapp);
 			}
		/*	frechet=fopen(FRECHET,"w");
			fdelta=fopen(FDELTA,"w");
			for(i=0;i<sumnmax+sumcountdt;i++)fprintf(frechet,"%d %f\n",sfrenum[i],sfrelen[i]);
			for(i=0;i<sumcountdt;i++)fprintf(fdelta,"%f\n",sdeltat[i]);
			fclose(frechet);fclose(fdelta);
			frechetapp=fopen(FRECHETAPP,"w");
			fdeltaapp=fopen(FDELTAAPP,"w");
			for(i=0;i<sumnmaxapp+sumcountdtapp;i++)fprintf(frechetapp,"%d %f\n",sfrenumapp[i],sfrelenapp[i]);
			for(i=0;i<sumcountdtapp;i++)fprintf(fdeltaapp,"%f\n",sdeltatapp[i]);
			fclose(frechetapp);fclose(fdeltaapp);	*/
 		
			for(i=0;i<sumcountdt;i++)sumdelta=sumdelta+sdeltat[i]*sdeltat[i];
//			sumdelta=sqrt(sumdelta)/sumcountdt;
			if(iter==0)initdelta=sumdelta;
			printf("the delta t of iteration %d is %f\n",iter+1,sumdelta/initdelta);

			for(i=0;i<nx;i++)
				for(j=0;j<ny;j++)
					for(k=0;k<nz;k++)
						sel3D[i][j][k]=(1000/vel3D[i][j][k]);
	/* the LSQR with Tikhonov regularization */
			RegLSQR(sumcountdt,sumnmax,sumcountdtapp,sumnmaxapp,sign,nx,ny,nz,damp,lamda,sz,omega,itmax,nx*ny*nz,sdeltat,sfrenum,sfrelen,ds,sel3D,sdeltatapp,sfrenumapp,sfrelenapp,dens);
	/* simple mean smoothing */		
			smooth(vel3D,ds,nx,ny,nz);

			for(i=0;i<nx;i++)
				for(j=0;j<ny;j++)
					for(k=0;k<nz;k++)
                   	 if(k<(int)(ele[i][j]/dz))
                     		{vel3D[i][j][k]=340;}

			velupdate=fopen("velupdate.dat","wb+");

			for(i=0;i<nx;i++)
				for(j=0;j<ny;j++)
					for(k=0;k<nz;k++)
                                      {
						fwrite(&vel3D[i][j][k],sizeof(float),1,velupdate); 

                                      }
			fclose(velupdate);//fclose(epsupdate);fclose(detaupdate);
		}


		MPI_Barrier(MPI_COMM_WORLD);

	} 
	/* iteration end */
	if(myid==0){
		for(i=0;i<nx;i++)
			for(j=0;j<ny;j++)
				for(k=0;k<nz;k++)
					fwrite(&dens[i][j][k],sizeof(float),1,fdensity);
			}
	fclose(fdensity);
	if(myid==0){printf("=Now the 3D First Break End, Please Check the Vel and Density=\n");}
	MPI_Finalize();
	exit(0);
}
int *readpar(int *nshot,int *nray,int *nx,int *ny,int *nz,float *dx,float *dy,float *dz,float *v0,float *dv,float *delta,int *sign,float *damp,float *lamda,float *sz,float *omega,int *itmax,int *niter,char *cele,char *cshot,char *crec,char *ccount)
{
	int i,*neachshot;
	FILE *fpar,*fcount;
	fpar=fopen("Tomo3D.par","r");
//	fscanf(fpar,"%s\n",cele);
	strcpy(cele,"elevation.dat");
//	fscanf(fpar,"%s\n",cshot);
	strcpy(cshot,"shot.txt");
//	fscanf(fpar,"%s\n",crec);
	strcpy(crec,"rec.txt");
//	fscanf(fpar,"%s\n",ccount);
	strcpy(ccount,"count.txt");
	fcount=fopen(ccount,"r");
	fscanf(fpar,"%d\n",nshot);
	neachshot=sf_intalloc(*nshot);
	fscanf(fpar,"%d\n",nx);
	fscanf(fpar,"%d\n",ny);
	fscanf(fpar,"%d\n",nz);
	fscanf(fpar,"%f\n",dx);
	fscanf(fpar,"%f\n",dy);
	fscanf(fpar,"%f\n",dz);
	fscanf(fpar,"%f\n",v0);
	fscanf(fpar,"%f\n",dv);
	fscanf(fpar,"%f\n",delta);
//	fscanf(fpar,"%d\n",sign);
	*sign=1;
	fscanf(fpar,"%f\n",damp);
	fscanf(fpar,"%f\n",lamda);
	fscanf(fpar,"%f\n",sz);
	fscanf(fpar,"%f\n",omega);
	fscanf(fpar,"%d\n",itmax);
	fscanf(fpar,"%d\n",niter);
	for(i=0;i<*nshot;i++)fscanf(fcount,"%d",&neachshot[i]);
	for(i=0;i<*nshot;i++)*nray=*nray+neachshot[i];
	return neachshot;          
}
int sum(int *neachshot,int is)
{
	int i,s=0;
	for(i=0;i<is;i++)
		s=s+neachshot[i];
	return s;
}

void buildtomo(float *vel,float *vx,float *q,float ***eps,float ***deta,float ***vel3D,float ***vel_x3D,float ***vel_q3D,int nx,int ny,int nz,float dx,float dy,float dz,float v0,float dv,int nshot,int nray,char *cele,char *cshot,char *crec,char *ccount,float **ele,float **shotxyz,float **recxyz,int *neachshot,float *eps1,float *deta1)
{
	int i,j,k,count=0;
	int tempx,tempy;
	FILE *fele,*fshot,*frec,*fcount,*bp1,*bp2,*bp3;
	fele=fopen(cele,"rb");
//	fp=fopen("amoco3d.dat","rb");

	for(i=0;i<nx;i++)
		for(j=0;j<ny;j++)
			{fread(&ele[i][j],sizeof(float),1,fele);}

	for(i=0;i<nx;i++)
	{
		for(j=0;j<ny;j++)
		{
			for(k=0;k<nz;k++)
			{

				if(k<(int)(ele[i][j]/dz))
					{vel3D[i][j][k]=340;}

				        else
					 {vel3D[i][j][k]=v0+k*dv;} 
				        vel[count]=(1/vel3D[i][j][k])*(1/vel3D[i][j][k]);
				        eps[i][j][k]=vel3D[i][j][k]/15000;
                                deta[i][j][k]=vel3D[i][j][k]/30000;
                                q[count]=(1+2*deta[i][j][k])/(1+2*eps[i][j][k]);
                                vx[count]=vel[count]/(1+2*eps[i][j][k]);      
		        	count++;
			}
		}			
	} 

	fshot=fopen(cshot,"r");
	for(i=0;i<nshot;i++)
	{
		fscanf(fshot,"%f %f\n",&shotxyz[i][0],&shotxyz[i][1]);
		tempx=(int)(shotxyz[i][0]/dx+0.5);tempy=(int)(shotxyz[i][1]/dy+0.5);
		shotxyz[i][2]=ele[tempx][tempy];
	}
	frec=fopen(crec,"r");
	for(i=0;i<nray;i++)
	{
		fscanf(frec,"%f %f\n",&recxyz[i][0],&recxyz[i][1]);
		tempx=(int)(recxyz[i][0]/dx+0.5);tempy=(int)(recxyz[i][1]/dy+0.5);
		recxyz[i][2]=ele[tempx][tempy];
	}
	fcount=fopen(ccount,"r");
	for(i=0;i<nshot;i++)
		fscanf(fcount,"%d\n",&neachshot[i]);	
}

void buildtomo1(float *realvel,float *realvx,float *realq,float ***realeps,float ***realdeta,float ***realvel3D,int nx,int ny,int nz,float dx,float dy,float dz,float v0,float dv,int nshot,int nray,char *cele,char *cshot,char *crec,char *ccount,float **ele,float **shotxyz,float **recxyz,int *neachshot)
{
	int i,j,k,count=0,d;
	int tempx,tempy;
	FILE *fele,*fshot,*frec,*fcount,*bp4,*bp5,*bp6;
	fele=fopen(cele,"rb");
//	fp=fopen("amoco3d.dat","rb");     
      bp4=fopen("velmodel_bp.dat","rb");
      bp5=fopen("epsilon_bp.dat","rb");
      bp6=fopen("delta_bp.dat","rb");
	for(i=0;i<nx;i++)
		for(j=0;j<ny;j++)
			{fread(&ele[i][j],sizeof(float),1,fele);}

	for(i=0;i<nx;i++)
	{
		for(j=0;j<ny;j++)
		{
			for(k=0;k<nz;k++)
			{
				fread(&realvel3D[i][j][k],sizeof(float),1,bp4);
				fread(&realdeta[i][j][k],sizeof(float),1,bp5);
				fread(&realeps[i][j][k],sizeof(float),1,bp6);

				        realvel[count]=(1/realvel3D[i][j][k])*(1/realvel3D[i][j][k]);
                                realq[count]=(1+2*realdeta[i][j][k])/(1+2*realeps[i][j][k]);
                                realvx[count]=realvel[count]/(1+2*realeps[i][j][k]);      
		        		  count++;
			}
		}			
	}  


}
void appvel(int nx,int ny,int nz,int js,float **recxyz,FILE *frechetapp,FILE *fdeltaapp,int *nmaxapp,int *countdtapp,float dt1,float dt2,int *gArray1,float *freArray1,int cal1,int *gArray2,float *freArray2,int cal2)
{
	int i,j,k,siren=0,igrid,barnum=-1;
	float dt,dx,temp=0,barlen=0;

	dt=dt1-dt2;
	dx=sqrt((recxyz[js][0]-recxyz[js-1][0])*(recxyz[js][0]-recxyz[js-1][0])+(recxyz[js][1]-recxyz[js-1][1])*(recxyz[js][1]-recxyz[js-1][1])+(recxyz[js][2]-recxyz[js-1][2])*(recxyz[js][2]-recxyz[js-1][2]));

/*	  for(k=0;k<nz;k++)
		   for(j=0;j<ny;j++)
			  for(i=0;i<nx;i++)
				length[i][j][k]=length1[i][j][k]-length2[i][j][k];

		for(k=0;k<nz;k++)
		   for(j=0;j<ny;j++)
			  for(i=0;i<nx;i++)
			  {
              if(fabs(length[i][j][k])>1e-6)
                {
                 igrid=k*nx*ny+j*nx+i;
                 fprintf(frechetapp,"%d %f\n",igrid,length[i][j][k]/dx);
                 *nmaxapp=*nmaxapp+1;
                 siren=1;
                }
			  }
         if(siren==1)
        {
         fprintf(frechetapp,"%d %d\n",-1,0);      
        *countdtapp=*countdtapp+1;
        fprintf(fdeltaapp,"%f\n",dt/dx);
        } */

	if(cal1!=0&&cal2!=0)
	{
		for(i=0;i<cal1;i++)
		{
			if(fabs(freArray1[i])>1e-6)
			{
				fwrite(&gArray1[i],sizeof(int),1,frechetapp);
				temp=freArray1[i]/dx;
				fwrite(&temp,sizeof(float),1,frechetapp);
//				fprintf(frechetapp,"%d %f\n",gArray1[i],freArray1[i]/dx);
 				*nmaxapp=*nmaxapp+1;
			 	siren=1;
			}
		}
		for(i=0;i<cal2;i++)
		{
		 	if(fabs(freArray2[i])>1e-6)
			{
				fwrite(&gArray2[i],sizeof(int),1,frechetapp);
				temp=-freArray2[i]/dx;
				fwrite(&temp,sizeof(float),1,frechetapp);
//				fprintf(frechetapp,"%d %f\n",gArray2[i],-freArray2[i]/dx);
 				*nmaxapp=*nmaxapp+1;
				 siren=1;
			}
		}
         if(siren==1)
        {
			fwrite(&barnum,sizeof(int),1,frechetapp);
			fwrite(&barlen,sizeof(float),1,frechetapp);
//         		fprintf(frechetapp,"%d %f\n",-1,0.);      
			*countdtapp=*countdtapp+1;
			temp=dt/dx;
			fwrite(&temp,sizeof(float),1,fdeltaapp);
//			fprintf(fdeltaapp,"%f\n",dt/dx);
        }
	} 
}

float norm3(float *a) { return sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2]); }

int checkBounds3d( float *point, int *Isize,float dx,float dy,float dz) {
    if((point[0]<0)||(point[1]<0)||(point[2]<0)||(point[0]>(Isize[0]-1)*dx)||(point[1]>(Isize[1]-1)*dy)||(point[2]>(Isize[2]-1)*dz)) { return false; }
    return true;
}

int mindex3(int x, int y, int z, int sizx, int sizy)  { return z*sizy*sizx+y*sizx+x;}

int shortestpath(float ***time,float *StartPoint,float *SourcePoint,float Stepsize,float *gradientArray,int nx,int ny,int nz,float dx,float dy,float dz,FILE *frechet,FILE *fdelta,int *nmax,int *countdt,FILE *fp1,FILE *fp2,FILE *fp3,int myid,int numprocs,float dt,int *gArraym,float *freArraym,float *freArraym_x,float *freArraym_z,float *freArraym_e,int *calm,float *eps1,float *deta1,float *vel)
{
	int i=0,j,k,ifree=(int)(2*sqrt((nx*dx)*(nx*dx)+(ny*dy)*(ny*dy)+(nz*dz)*(nz*dz))/Stepsize),flag=0,igrid,siren=0,barnum=-1;
	int sfregridx,sfregridy,sfregridz;
	int nfregridx,nfregridy,nfregridz;
	float nextpoint[3]={0},DistancetoEnd,Movement,**ShortestLine,barlen=0;
	float l=0;
	int *gArray;
	float *freArray,*freArray_x,*freArray_z,*freArray_e,*theta;
	int cal=0;
      float A;

	i=0;
	ShortestLine=sf_floatalloc2(3,ifree);
	freArray=sf_floatalloc(ifree);
	freArray_x=sf_floatalloc(ifree);
	freArray_z=sf_floatalloc(ifree);
	freArray_e=sf_floatalloc(ifree);
	gArray=sf_intalloc(ifree);
      theta=sf_floatalloc(ifree);

	rk4(StartPoint,gradientArray,Stepsize,nx,ny,nz,dx,dy,dz,nextpoint);
	ShortestLine[0][0]=StartPoint[0];ShortestLine[0][1]=StartPoint[1];ShortestLine[0][2]=StartPoint[2];
	
	while(fabs(nextpoint[0])>1e-6)
	{
		sfregridx=(int)((StartPoint[0]-dx)/(dx));sfregridy=(int)((StartPoint[1]-dy)/(dy));sfregridz=(int)((StartPoint[2]-dz)/(dz));
		nfregridx=(int)((nextpoint[0]-dx)/(dx));nfregridy=(int)((nextpoint[1]-dy)/(dy));nfregridz=(int)((nextpoint[2]-dz)/(dz));
		if((sfregridx==nfregridx)&&(sfregridy==nfregridy)&&(sfregridz==nfregridz))
		{
			l=l+sqrt((StartPoint[0]-nextpoint[0])*(StartPoint[0]-nextpoint[0])+(StartPoint[1]-nextpoint[1])*(StartPoint[1]-nextpoint[1])+(StartPoint[2]-nextpoint[2])*(StartPoint[2]-nextpoint[2]));
                  theta[cal]=atan((StartPoint[2]-nextpoint[2])/l);
              
		}
		else
		{
			l=l+sqrt((StartPoint[0]-dx-(StartPoint[0]-dx+nextpoint[0]-dx)/2)*(StartPoint[0]-dx-(StartPoint[0]-dx+nextpoint[0]-dx)/2)+(StartPoint[1]-dy-(StartPoint[1]-dy+nextpoint[1]-dy)/2)*(StartPoint[1]-dy-(StartPoint[1]-dy+nextpoint[1]-dy)/2)+(StartPoint[2]-dz-(StartPoint[2]-dz+nextpoint[2]-dz)/2)*(StartPoint[2]-dz-(StartPoint[2]-dz+nextpoint[2]-dz)/2));
			igrid=sfregridz*nx*ny+sfregridy*nx+sfregridx;
                  gArray[cal]=igrid;freArray[cal]=l;cal++;
    		
			l=0;
			l=l+sqrt((nextpoint[0]-dx-(StartPoint[0]-dx+nextpoint[0]-dx)/2)*(nextpoint[0]-dx-(StartPoint[0]-dx+nextpoint[0]-dx)/2)+(nextpoint[1]-dy-(StartPoint[1]-dy+nextpoint[1]-dy)/2)*(nextpoint[1]-dy-(StartPoint[1]-dy+nextpoint[1]-dy)/2)+(nextpoint[2]-dz-(StartPoint[2]-dz+nextpoint[2]-dz)/2)*(nextpoint[2]-dz-(StartPoint[2]-dz+nextpoint[2]-dz)/2));
                  theta[cal]=atan((nextpoint[2]-dz-(StartPoint[2]-dz+nextpoint[2]-dz)/2)*(nextpoint[2]-dz-(StartPoint[2]-dz+nextpoint[2]-dz)/2)/l);
		}


		DistancetoEnd=sqrt((SourcePoint[0]-nextpoint[0])*(SourcePoint[0]-nextpoint[0])+(SourcePoint[1]-nextpoint[1])*(SourcePoint[1]-nextpoint[1])+(SourcePoint[2]-nextpoint[2])*(SourcePoint[2]-nextpoint[2]));

		if(DistancetoEnd<Stepsize){break;}

		if(i>10)
		Movement=sqrt((nextpoint[0]-ShortestLine[i-10][0])*(nextpoint[0]-ShortestLine[i-10][0])+(nextpoint[1]-ShortestLine[i-10][1])*(nextpoint[1]-ShortestLine[i-10][1])+(nextpoint[2]-ShortestLine[i-10][2])*(nextpoint[2]-ShortestLine[i-10][2]));
		else Movement=Stepsize;
		if(Movement<Stepsize)break;

		i++;
		ShortestLine[i][0]=nextpoint[0];ShortestLine[i][1]=nextpoint[1];ShortestLine[i][2]=nextpoint[2];
//  	write the ray path 
//		if(myid==0){fprintf(fp1,"%f\n",ShortestLine[i][0]);fprintf(fp2,"%f\n",ShortestLine[i][1]);fprintf(fp3,"%f\n",ShortestLine[i][2]);}


		StartPoint[0]=nextpoint[0];StartPoint[1]=nextpoint[1];StartPoint[2]=nextpoint[2];
		rk4(StartPoint,gradientArray,Stepsize,nx,ny,nz,dx,dy,dz,nextpoint);

		if(i==ifree-1){flag=1;break;}
	  
	}
	if(i!=0)
	{
		if((sfregridx==nfregridx)&&(sfregridy==nfregridy)&&(sfregridz==nfregridz))
		{
			igrid=sfregridz*nx*ny+sfregridy*nx+sfregridx;
            gArray[cal]=igrid;freArray[cal]=l;cal++;
		}
		else
		{
			igrid=nfregridz*nx*ny+nfregridy*nx+nfregridx;
            gArray[cal]=igrid;freArray[cal]=l;cal++;
		}
	}
	
//	if(cal==0){printf("****%d\n",i);system("pause");}
	if(flag==0&&cal!=0)
	{
		*calm=cal;
		for(i=0;i<cal;i++)
		{
		 	if(fabs(freArray[i])>1e-6)
			{
			gArraym[i]=gArray[i];         //hangliehao
                  freArraym[i]=freArray[i];
              //    A=sqrt(((1/(1+2*deta1[i])-2/(1+2*eps1[i])+1)*cos(theta[i]))*cos(theta[i])-(1/(1+2*deta1[i])-1/(1+2*eps1[i]))*cos(theta[i])*cos(theta[i])*cos(theta[i])*cos(theta[i])+1/(1+2*eps1[i]));
              //    freArray_z[i]=freArray[i]*A;
              //    freArray_x[i]=freArray[i]*(sin(theta[i])*sin(theta[i])+2*eps1[i]*cos(theta[i])*cos(theta[i])+cos(theta[i])*cos(theta[i])*cos(theta[i])*cos(theta[i]))/(sqrt(1+2*eps1[i])*A);//I
             //     freArray_e[i]=freArray[i]*(cos(theta[i])*cos(theta[i])-cos(theta[i])*cos(theta[i])*cos(theta[i])*cos(theta[i])+1)*sqrt(vel[i])/A;
			fwrite(&gArray[i],sizeof(int),1,frechet);
			fwrite(&freArray[i],sizeof(float),1,frechet);
		//	fprintf(frechet,"%d %f %f %f %f\n",gArray[i],freArray[i],freArray_x[i],freArray_z[i],freArray_e[i]);
               //   printf("%d %f %f %f %f\n",gArray[i],freArray[i],freArray_x[i],freArray_z[i],freArray_e[i]);
 			*nmax=*nmax+1;
			 siren=1;
			}
		}
		if(siren==1)
		{
			fwrite(&barnum,sizeof(int),1,frechet);
			fwrite(&barlen,sizeof(float),1,frechet);//fengehang-1,0
		//	fprintf(frechet,"%d %f %f %f %f\n",-1,0.,0.,0.,0.);      
			*countdt=*countdt+1;
			fwrite(&dt,sizeof(float),1,fdelta);
//			fprintf(fdelta,"%f\n",dt);
		}

	} 

	free(ShortestLine[0]);
	free(ShortestLine);
	free(freArray);free(gArray);//free(freArray_x);free(freArray_z);free(freArray_e);
	return siren;
}
void rk4(float *startPoint,float *gradientArray,float StepSize,int nx,int ny,int nz,float dx,float dy,float dz,float *nextPoint)
{
	int gradientArraySize[3];
	float startPoint1[3];
	gradientArraySize[0]=nx;gradientArraySize[1]=ny;gradientArraySize[2]=nz;
	startPoint1[0]=startPoint[0]-dx; startPoint1[1]=startPoint[1]-dy; startPoint1[2]=startPoint[2]-dz;
	if(RK4STEP_3D(gradientArray, gradientArraySize, startPoint1, nextPoint, StepSize,dx,dy,dz)) {
		nextPoint[0]=nextPoint[0]+dx;nextPoint[1]=nextPoint[1]+dy;nextPoint[2]=nextPoint[2]+dz;
		}
	else {
		nextPoint[0]=0; nextPoint[1]=0; nextPoint[2]=0;
		}
 }

bool RK4STEP_3D(float *gradientArray, int *gradientArraySize, float *startPoint, float *nextPoint, float stepSize,float dx,float dy,float dz) {
    float k1[3], k2[3], k3[3], k4[3];
    float tempPoint[3];
    float tempnorm;
    
	interpgrad3d(k1, gradientArray, gradientArraySize, startPoint,dx,dy,dz);

    tempnorm=norm3(k1);
    k1[0] = k1[0]*stepSize/tempnorm;
    k1[1] = k1[1]*stepSize/tempnorm;
    k1[2] = k1[2]*stepSize/tempnorm;
    
    tempPoint[0]=startPoint[0] - k1[0]*0.5;
    tempPoint[1]=startPoint[1] - k1[1]*0.5;
    tempPoint[2]=startPoint[2] - k1[2]*0.5;
            
    if (!checkBounds3d(tempPoint, gradientArraySize,dx,dy,dz)) return false;
    
    interpgrad3d(k2, gradientArray, gradientArraySize, tempPoint,dx,dy,dz);
    tempnorm=norm3(k2);

    k2[0] = k2[0]*stepSize/tempnorm;
    k2[1] = k2[1]*stepSize/tempnorm;
    k2[2] = k2[2]*stepSize/tempnorm;
    
    tempPoint[0]=startPoint[0] - k2[0]*0.5;
    tempPoint[1]=startPoint[1] - k2[1]*0.5;
    tempPoint[2]=startPoint[2] - k2[2]*0.5;
    
    if (!checkBounds3d(tempPoint, gradientArraySize,dx,dy,dz)) return false;
    
    interpgrad3d(k3, gradientArray, gradientArraySize, tempPoint,dx,dy,dz);
    tempnorm=norm3(k3);
    k3[0] = k3[0]*stepSize/tempnorm;
    k3[1] = k3[1]*stepSize/tempnorm;
    k3[2] = k3[2]*stepSize/tempnorm;
        
    tempPoint[0]=startPoint[0] - k3[0];
    tempPoint[1]=startPoint[1] - k3[1];
    tempPoint[2]=startPoint[2] - k3[2];
    
    if (!checkBounds3d(tempPoint, gradientArraySize,dx,dy,dz)) return false;
    
    interpgrad3d(k4, gradientArray, gradientArraySize, tempPoint,dx,dy,dz);
    tempnorm=norm3(k4);
    k4[0] = k4[0]*stepSize/tempnorm;
    k4[1] = k4[1]*stepSize/tempnorm;
    k4[2] = k4[2]*stepSize/tempnorm;
    
    nextPoint[0] = startPoint[0] - (k1[0] + k2[0]*2.0 + k3[0]*2.0 + k4[0])/6.0;
    nextPoint[1] = startPoint[1] - (k1[1] + k2[1]*2.0 + k3[1]*2.0 + k4[1])/6.0;
    nextPoint[2] = startPoint[2] - (k1[2] + k2[2]*2.0 + k3[2]*2.0 + k4[2])/6.0;
     
    if (!checkBounds3d(nextPoint, gradientArraySize,dx,dy,dz)) return false;
    
    return true;
}
void interpgrad3d(float *Ireturn, float *Grad, int *Isize, float *point,float dx,float dy,float dz) {

    int xBas0, xBas1, yBas0, yBas1, zBas0, zBas1;
    float perc[8];
    float xCom, yCom, zCom;
    float xComi, yComi, zComi;
    float fTlocalx, fTlocaly, fTlocalz;
    int f0, f1;
    int index[8];
    float temp;

    fTlocalx = floor(point[0]/dx); fTlocaly = floor(point[1]/dy); fTlocalz = floor(point[2]/dz);
    xBas0=(int) fTlocalx; yBas0=(int) fTlocaly; zBas0=(int) fTlocalz;
    xBas1=xBas0+1; yBas1=yBas0+1; zBas1=zBas0+1;
    
    xCom=point[0]-fTlocalx*dx;  yCom=point[1]-fTlocaly*dy;   zCom=point[2]-fTlocalz*dz;
    xComi=(dx-xCom); yComi=(dy-yCom); zComi=(dz-zCom);
    perc[0]=xComi * yComi; perc[1]=perc[0] * zCom; perc[0]=perc[0] * zComi;
    perc[2]=xComi * yCom;  perc[3]=perc[2] * zCom; perc[2]=perc[2] * zComi;
    perc[4]=xCom * yComi;  perc[5]=perc[4] * zCom; perc[4]=perc[4] * zComi;
    perc[6]=xCom * yCom;   perc[7]=perc[6] * zCom; perc[6]=perc[6] * zComi;
    
    if(xBas0<0) { xBas0=0; if(xBas1<0) { xBas1=0; }}
    if(yBas0<0) { yBas0=0; if(yBas1<0) { yBas1=0; }}
    if(zBas0<0) { zBas0=0; if(zBas1<0) { zBas1=0; }}
    if(xBas1>(Isize[0]-1)) { xBas1=Isize[0]-1; if(xBas0>(Isize[0]-1)) { xBas0=Isize[0]-1; }}
    if(yBas1>(Isize[1]-1)) { yBas1=Isize[1]-1; if(yBas0>(Isize[1]-1)) { yBas0=Isize[1]-1; }}
    if(zBas1>(Isize[2]-1)) { zBas1=Isize[2]-1; if(zBas0>(Isize[2]-1)) { zBas0=Isize[2]-1; }}
    
    index[0]=mindex3(xBas0, yBas0, zBas0, Isize[0], Isize[1]);
    index[1]=mindex3(xBas0, yBas0, zBas1, Isize[0], Isize[1]);
    index[2]=mindex3(xBas0, yBas1, zBas0, Isize[0], Isize[1]);
    index[3]=mindex3(xBas0, yBas1, zBas1, Isize[0], Isize[1]);
    index[4]=mindex3(xBas1, yBas0, zBas0, Isize[0], Isize[1]);
    index[5]=mindex3(xBas1, yBas0, zBas1, Isize[0], Isize[1]);
    index[6]=mindex3(xBas1, yBas1, zBas0, Isize[0], Isize[1]);
    index[7]=mindex3(xBas1, yBas1, zBas1, Isize[0], Isize[1]);
    f0=Isize[0]*Isize[1]*Isize[2];
    f1=f0+f0;
    
    temp=Grad[index[0]]*perc[0]+Grad[index[1]]*perc[1]+Grad[index[2]]*perc[2]+Grad[index[3]]*perc[3];
    Ireturn[0]=temp+Grad[index[4]]*perc[4]+Grad[index[5]]*perc[5]+Grad[index[6]]*perc[6]+Grad[index[7]]*perc[7];
    temp=Grad[index[0]+f0]*perc[0]+Grad[index[1]+f0]*perc[1]+Grad[index[2]+f0]*perc[2]+Grad[index[3]+f0]*perc[3];
    Ireturn[1]=temp+Grad[index[4]+f0]*perc[4]+Grad[index[5]+f0]*perc[5]+Grad[index[6]+f0]*perc[6]+Grad[index[7]+f0]*perc[7];
    temp=Grad[index[0]+f1]*perc[0]+Grad[index[1]+f1]*perc[1]+Grad[index[2]+f1]*perc[2]+Grad[index[3]+f1]*perc[3];
    Ireturn[2]=temp+Grad[index[4]+f1]*perc[4]+Grad[index[5]+f1]*perc[5]+Grad[index[6]+f1]*perc[6]+Grad[index[7]+f1]*perc[7];
}
void laplace(float ***time,int nx,int ny,int nz,float dx,float dy,float dz,float ***gx,float ***gy,float ***gz)
{
	int i,j,k;
	for(i=0;i<nx;i++)
		for(j=0;j<ny;j++)
			for(k=0;k<nz;k++)
			{
				if(i==0)
					gx[i][j][k]=(time[i+1][j][k]-time[i][j][k])/dx;
				else if(i==nx-1)
                    gx[i][j][k]=(time[i][j][k]-time[i-1][j][k])/dx;
				else
					gx[i][j][k]=(time[i+1][j][k]-time[i-1][j][k])/(2*dx);
			}
	for(i=0;i<nx;i++)
		for(j=0;j<ny;j++)
			for(k=0;k<nz;k++)
			{
				if(j==0)
					gy[i][j][k]=(time[i][j+1][k]-time[i][j][k])/dy;
				else if(j==ny-1)
                    gy[i][j][k]=(time[i][j][k]-time[i][j-1][k])/dy;
				else
					gy[i][j][k]=(time[i][j+1][k]-time[i][j-1][k])/(2*dy);
			}
	for(i=0;i<nx;i++)
		for(j=0;j<ny;j++)
			for(k=0;k<nz;k++)
			{
				if(k==0)
					gz[i][j][k]=(time[i][j][k+1]-time[i][j][k])/dz;
				else if(k==nz-1)
                    gz[i][j][k]=(time[i][j][k]-time[i][j][k-1])/dz;
				else
					gz[i][j][k]=(time[i][j][k+1]-time[i][j][k-1])/(2*dz);
			}

}

static void regul(int nx,int ny,int nz,int rr,int  layer_cell_num,float damp,float lamda,float sz,int *k,int *row,int *col,float *val,int *layer_cell,int nmax,float ***vel3D,float *dt,float *sumreg,float ***dens);
static void ap(int kp,float temp,int *k,int *col,float *val,int nmax);
static void normlz(int n,float *x,float *s);
static void CRS_mv(float *val,int *col,int *row,float *b,float *c,int m);
static void CRS_mtv(float *val,int *col,int *row,float *c,float *b,int m,int n);
static void avpu_compress(int m,int n,float *u,float *v,float *val,int *col,int *row,int nmax);
static void atupv_compress(int m,int n,float *u,float *v,float *val,int *col,int *row,int nmax);
static void lsqr_compress(int m,int n,float *x,float *u,int itmax,float *val,
	int *col,int *row,int nmax);
void  RegLSQR(int nrays,int nmax,int nraysapp,int nmaxapp,int sign,int nx,int ny,int nz,float damp,float lamda,float sz,float omega,int itmax,int layer_cell_num,float *deltat,int *frenum,float *frelen,float *ds,float ***sel3D,float *deltatapp,int *frenumapp,float *frelenapp,float ***dens) 
{ 
	int   i,k,j,p,ok,kp,count=0; 
	int   *layer_cell,*col,*row; 
	float temp; 
	float *dt,*val; 
	int   rr,raynum,gx,gy,gz;  
	float *derr; 
	float *lens;
	float sumdt=0,sumdtapp=0,sumreg=0;
	float minlens=9999,iminlens,maxlens=0,imaxlens;

	for(i=0;i<nx;i++)
		for(j=0;j<ny;j++)
			for(p=0;p<nz;p++)
				dens[i][j][p]=0.;
	printf("***************TOMO BEGIN***************\n");

	printf("nrays=%d,nraysapp=%d,nmax=%d,nmaxapp=%d,sign=%d,nx=%d,ny=%d,nz=%d\n",nrays,nraysapp,nmax,nmaxapp,sign,nx,ny,nz);
	lens=(float*)malloc(sizeof(float)*nrays);
	for(i=0;i<nrays;i++)lens[i]=0;
	raynum=nrays;
	rr=nrays+nraysapp;      	
	
	/* read layer_cell_num */

	printf("layer_cell_num====%d\n",layer_cell_num);
    
	/* regularizion */
	if(sign==1)
	{   
		nrays=nrays+nraysapp+3*layer_cell_num;
	    nmax=nmax+nmaxapp+9*layer_cell_num;
        printf("sign===1,nrays(reg)=%d,reg nmax(reg)=%d\n",nrays,nmax);
		derr=(float*)malloc(sizeof(float)*nrays);
	}
	
	/* malloc space */
	dt=(float*)malloc(sizeof(float)*nrays);
	layer_cell=(int*)malloc(sizeof(int)*layer_cell_num);

	/* read order number of the cell in the layer */
    for(i=0;i<layer_cell_num;i++)
	{
		layer_cell[i]=i+1;
	}
	/**************************/
	count=0;
	for(i=0;i<raynum;i++) 
	{ 	 
b:	    kp=frenum[count];
		if(kp!=-1)  
		{	 
			temp=frelen[count];
			lens[i]=lens[i]+temp;
			count++;
			goto b; 
		} 
		count++;
	} 

	for(i=0;i<raynum;i++) 
	{
		if(lens[i]<minlens){minlens=lens[i];iminlens=i;}
		if(lens[i]>maxlens){maxlens=lens[i];imaxlens=i;}
	}

	for(i=0;i<raynum;i++)
	{
		if(lens[i]>1e-6) 		
		dt[i]=deltat[i]/lens[i]*1000;
		else
		dt[i]=deltat[i]*1000;
		sumdt=sumdt+dt[i];
	}
	free(deltat);

	for(i=raynum;i<rr;i++)
	{ 		
		dt[i]=deltatapp[i-raynum]*1000*omega;
		sumdtapp=sumdtapp+dt[i];
	}
	free(deltatapp);

	val=(float*)malloc(sizeof(float)*nmax);
	col=(int*)malloc(sizeof(int)*nmax);
	row=(int*)malloc(sizeof(int)*(nrays+1));

  /* read data of CRS */
	row[0]=0;count=0;
	k=0;
	for(i=0;i<raynum;i++) 
	{ 
		 
a:	    kp=frenum[count];
		if(kp!=-1)  
		{	 
		    if(lens[i]>1e-6) 		
		    temp=frelen[count]/lens[i];
		    else
		    temp=frelen[count];
		    gz=(int)(kp/(nx*ny));
		    gy=(int)((kp-gz*(nx*ny))/nx);
		    gx=kp-gz*(nx*ny)-gy*nx;
			dens[gx][gy][gz]++;
			ok=0; 
//			kp=kp-1;
			ap(kp,(float)temp,&k,col,val,nmax);
			count++;
			goto a; 
		} 
		count++;
		row[i+1]=k; 
	}
          //  free(frenum);free(frelen); 

	count=0;
	for(i=raynum;i<rr;i++) 
	{ 
		 
c:	    kp=frenumapp[count];
		if(kp!=-1)  
		{	if(count>=nraysapp+nmaxapp){printf("error report\n");system("pause");} 
			temp=frelenapp[count]*omega;
			ok=0; 
//			kp=kp-1;
			ap(kp,(float)temp,&k,col,val,nmax);
			count++;
			goto c; 
		} 
		count++;
		row[i+1]=k; 
	} 
	printf("***************LSQR BEGIN***************\n");
	free(frenumapp);free(frelenapp);

	if(sign==1)
	{	  
		regul(nx,ny,nz,rr,layer_cell_num, damp,lamda,sz,&k,row,col,val,layer_cell,nmax,sel3D,dt,&sumreg,dens);
		lsqr_compress(nrays,layer_cell_num,ds,dt,itmax,val,col,row,nmax);
 	}
	else 
 	{   
	 	lsqr_compress(nrays,layer_cell_num,ds,dt,itmax,val,col,row,nmax);	
	}
	printf("***************LSQR END***************\n");	

	free(dt);free(lens);
	free(layer_cell);
	free(val);
	free(row);
	free(col);
	if(sign==1)free(derr);
}
void lsqr_compress(int m,int n,float *x,float *u,int itmax,float *val,int *col,int *row,int nmax)
{
	int i,iter;
	float beta,alfa;
	float b1,aa,b,c,r,s,t1,t2,p1,r1;
	float phibar,rho,rhobar,phi,teta;
	float *v,*w;
	float derr=0.000001;
	v=(float*)malloc(sizeof(float)*n);
	w=(float*)malloc(sizeof(float)*n);

	for(i=0;i<n;i++) { x[i]=0;v[i]=0; }
	normlz(m,u,&beta); b1=beta;
	atupv_compress(m,n,u,v,val,col,row,nmax); 
	normlz(n,v,&alfa);
	rhobar=alfa;phibar=beta; for(i=0;i<n;i++) { w[i]=v[i]; }
	r=phibar/b1;

	if(phibar<derr || r<derr) {printf("enough precise\n");goto mmm;}
	for(iter=0;iter<itmax;iter++)
	{
		if(iter%10==0)printf("LSQR has complished %f %%.Now phibar=%f r=%f\n",(float)(iter)/itmax*100,phibar,r);
		p1=phibar;r1=r;
		aa=-alfa; 
#pragma omp parallel for 
		for(i=0;i<m;i++) { u[i]=aa*u[i]; }
		avpu_compress(m,n,u,v,val,col,row,nmax); normlz(m,u,&beta);
		b=-beta;
#pragma omp parallel for 
		for(i=0;i<n;i++) { v[i]=b*v[i]; }
		atupv_compress(m,n,u,v,val,col,row,nmax); normlz(n,v,&alfa);
		rho=sqrt(rhobar*rhobar+beta*beta);
		c=rhobar/rho;s=beta/rho;teta=s*alfa;
		rhobar=-c*alfa;phi=c*phibar;phibar=s*phibar;
		t1=phi/rho;t2=-teta/rho;
#pragma omp parallel for 
		for(i=0;i<n;i++) { x[i]=t1*w[i]+x[i]; w[i]=t2*w[i]+v[i]; }
		r=phibar/b1;
		if(phibar<derr || r<derr) goto mmm;
		if(fabs(phibar-p1)<0.0001 && fabs(r-r1)<0.0001){printf("------");goto mmm;}
	}
mmm:	
	free(v);
	free(w);
}
static void avpu_compress(int m,int n,float *u,float *v,float *val,int *col,int *row,int nmax)
{
	//u=u+a*v
	int i;
	float *w; w=(float*)malloc(sizeof(float)*m);
	CRS_mv(val,col,row,v,w,m);
#pragma omp parallel for 
	for(i=0;i<m;i++) { u[i]=u[i]+w[i]; }
	free(w);
}

static void atupv_compress(int m,int n,float *u,float *v,float *val,int *col,int *row,int nmax)
{
	//v=v+at*u
	int j;
	float *w;w=(float*)malloc(sizeof(float)*n);
	CRS_mtv(val,col,row,u,w,m,n);
#pragma omp parallel for
	for(j=0;j<n;j++) { v[j]=v[j]+w[j]; }
	free(w);
}
static void CRS_mtv(float *val,int *col,int *row,float *c,float *b,int m,int n)
{
	int i,j;
#pragma omp parallel for
	for(i=0;i<n;i++) { b[i]=0; }
#pragma omp parallel for private(i,j)
	for(j=0;j<m;j++)
	{
		for(i=row[j];i<row[j+1];i++)
		{
			b[col[i]]=b[col[i]]+val[i]*c[j];
		}
	}
}
static void CRS_mv(float *val,int *col,int *row,float *b,float *c,int m)
{
	int i,j;
#pragma omp parallel for private(i,j)
	for(i=0;i<m;i++)
	{
		c[i]=0;
		for(j=row[i];j<row[i+1];j++)
		{
			c[i]=c[i]+val[j]*b[col[j]];
		}
	}
}
static void normlz(int n,float *x,float *s)
{
	int i;
	float temp=0;
	*s=0;
#pragma omp parallel for reduction(+:temp)
	for(i=0;i<n;i++)
	{
		temp=temp+pow(x[i],2);
	}
	*s=temp;
	*s=sqrt(*s);
#pragma omp parallel for
	for(i=0;i<n;i++)
	{
		x[i]=x[i]/(*s);
	}
}
static void ap(int kp,float temp,int *k,int *col,float *val,int nmax)
{
	col[*k]=kp;
	val[*k]=temp;
	*k=*k+1;
	if(*k>nmax){printf("k=%d k>=nmax error",*k);exit(0);}
}


static void regul(int nx,int ny,int nz,int rr,int  layer_cell_num,float damp,float lamda,float sz,int *k,int *row,int *col,float *val,int *layer_cell,int nmax,float ***sel3D,float *dt,float *sumreg,float ***dens)
{
	int i,j,p,kp;
	int gz,gy,gx;
	int siren=0;
	int current;
	float scentre,dtreg;
	float temp;
	float maxdens=0;
	
	for(i=0;i<nx;i++)
		for(j=0;j<ny;j++)
			for(p=0;p<nz;p++)
				if(dens[i][j][p]>maxdens)maxdens=dens[i][j][p];

	/* for damp */ 
	for(i=rr;i<rr+layer_cell_num;i++)
	{
		current=i-rr;dtreg=0;
		gz=(int)(current/(nx*ny));
		gy=(int)((current-gz*(nx*ny))/nx);
		gx=current-gz*(nx*ny)-gy*nx;
		scentre=sel3D[gx][gy][gz];
		kp=current;temp=damp*(dens[gx][gy][gz])/maxdens;///scentre;//kp=kp+1;
		ap(kp,(float)temp,k,col,val,nmax);
		row[i+1]=*k;
		dt[i]=0.0;
	}
	/* for horizontal */
	rr=rr+layer_cell_num;
	for(i=rr;i<rr+layer_cell_num;i++)
	{
		current=i-rr;siren=0;dtreg=0;
		gz=(int)(current/(nx*ny));
		gy=(int)((current-gz*(nx*ny))/nx);
		gx=current-gz*(nx*ny)-gy*nx;
		scentre=sel3D[gx][gy][gz];
		if(gx-1>=0){kp=(gx-1)+gy*nx+gz*(nx*ny);temp=lamda/scentre;ap(kp,(float)temp,k,col,val,nmax);siren++;dtreg=dtreg+temp*sel3D[gx-1][gy][gz];}
		if(gx+1<=nx-1){kp=(gx+1)+gy*nx+gz*(nx*ny);temp=lamda/scentre;ap(kp,(float)temp,k,col,val,nmax);siren++;dtreg=dtreg+temp*sel3D[gx+1][gy][gz];}
		if(gy-1>=0){kp=gx+(gy-1)*nx+gz*(nx*ny);temp=lamda/scentre;ap(kp,(float)temp,k,col,val,nmax);siren++;dtreg=dtreg+temp*sel3D[gx][gy-1][gz];}
		if(gy+1<=ny-1){kp=gx+(gy+1)*nx+gz*(nx*ny);temp=lamda/scentre;ap(kp,(float)temp,k,col,val,nmax);siren++;dtreg=dtreg+temp*sel3D[gx][gy+1][gz];}
		{kp=gx+gy*nx+gz*(nx*ny);temp=-siren*lamda/scentre;ap(kp,(float)temp,k,col,val,nmax);dtreg=dtreg+temp*sel3D[gx][gy][gz];}
		row[i+1]=*k;
		//dt[i]=-dtreg;
		dt[i]=0;	
		*sumreg=*sumreg+dt[i];
	}
	/* for vertical */
	rr=rr+layer_cell_num;
	for(i=rr;i<rr+layer_cell_num;i++)
	{
		current=i-rr;siren=0;dtreg=0;
		gz=(int)(current/(nx*ny));
		gy=(int)((current-gz*(nx*ny))/nx);
		gx=current-gz*(nx*ny)-gy*nx;
		scentre=sel3D[gx][gy][gz];
		if(gz-1>=0){kp=gx+gy*nx+(gz-1)*(nx*ny);temp=lamda*sz/scentre;ap(kp,(float)temp,k,col,val,nmax);siren++;dtreg=dtreg+temp*sel3D[gx][gy][gz-1];}
		if(gz+1<=nz-1){kp=gx+gy*nx+(gz+1)*(nx*ny);temp=lamda*sz/scentre;ap(kp,(float)temp,k,col,val,nmax);siren++;dtreg=dtreg+temp*sel3D[gx][gy][gz+1];}
		{kp=gx+gy*nx+gz*(nx*ny);temp=-siren*lamda*sz/scentre;ap(kp,(float)temp,k,col,val,nmax);dtreg=dtreg+temp*sel3D[gx][gy][gz];}
		row[i+1]=*k;
		//dt[i]=-dtreg;
		dt[i]=0;
		*sumreg=*sumreg+dt[i];
   }
}

void tripd2(float **d, float **e, float **b, int n, int m);
 
void vsm3d(float ***v,int n3,int n2,int n1,int iter,int depth,
	 float r3,float r2,float r1,float mu,int sl,float vmin,float vmax)
/***************************************************************************
Smooth 3d-velocity.  
*************************************************************************/
{
	int  i2, i1, i3, i;		
	float **d=NULL, **e=NULL, **f=NULL, *w, ww=1.0;
 
 /*	compute the weight function */
	w = sf_floatalloc(n1+n2+n3-2);
	if(depth==1){
		mu = (mu*mu-1.0)/(n1*n1);
		for(i1=0; i1<n1; ++i1) w[i1] = 1.0/(1+i1*i1*mu);
	}
	if(depth==2){
 		mu = (mu*mu-1.0)/(n2*n2);
		for(i2=0; i2<n2; ++i2) w[i2] = 1.0/(1+i2*i2*mu);
	}
	if(depth==3){
 		mu = (mu*mu-1.0)/(n3*n3);
		for(i3=0; i3<n3; ++i3) w[i3] = 1.0/(1+i3*i3*mu);
	}

/*	scale  smoothing parameters according to the iteration number	*/
	if(iter==1) {
		r1 /= 3.39*3.39;
		r2 /= 3.39*3.39;
		r3 /= 3.39*3.39;
	} else if(iter==2){
		r1 /= 5.19*5.19;
		r2 /= 5.19*5.19;
		r3 /= 5.19*5.19;
	} else {
		r1 /= 6.60*6.60;
		r2 /= 6.60*6.60;
		r3 /= 6.60*6.60;
	}


	/*  clip velocity  */
	for(i3=0; i3<n3; ++i3) 
	    for(i2=0; i2<n2; ++i2)
		for(i1=0; i1<n1; ++i1){
			if(v[i3][i2][i1] >vmax) v[i3][i2][i1] = vmax;
			if(v[i3][i2][i1] <vmin) v[i3][i2][i1] = vmin;
		}

	if(sl) {
	/*  smoothing on slowness  */
		for(i3=0; i3<n3; ++i3) 
			for(i2=0; i2<n2; ++i2)
				for(i1=0; i1<n1; ++i1)
					v[i3][i2][i1] = 1.0/v[i3][i2][i1];
	}
	

	if(r2>0.) {
 
/*	smoothing velocity in the second direction */

	/* allocate space */
 	d =sf_floatalloc2(n1,n2);
	e = sf_floatalloc2(n1,n2);
	f = sf_floatalloc2(n1,n2);
 
 
	for(i3=0; i3<n3; ++i3){
		if(depth==3) ww = w[i3];
	 	for(i2=0; i2<n2-1; ++i2){
			if(depth==2) ww = w[i2+1];
			for(i1=0; i1<n1; ++i1){
				if(depth==1) ww = w[i1];
				d[i2][i1] = ww+r2*2.0;
				e[i2][i1] = -r2;
 				f[i2][i1] = ww*v[i3][i2+1][i1];
			}
		}
			for(i1=0; i1<n1; ++i1){
	  		d[n2-2][i1] -= r2;
			f[0][i1] += r2*v[i3][0][i1];
  		}
	 	tripd2(d,e,f,n2-1,n1);

	    for(i=1; i<iter; ++i) {
	 	for(i2=0; i2<n2-1; ++i2){
			if(depth==2) ww = w[i2+1];
			for(i1=0; i1<n1; ++i1){
				if(depth==1) ww = w[i1];
				d[i2][i1] = ww+r2*2.0;
				e[i2][i1] = -r2;
 				f[i2][i1] *= ww;
			}
		}
			for(i1=0; i1<n1; ++i1){
	  		d[n2-2][i1] -= r2;
			f[0][i1] += r2*v[i3][0][i1];
  		}
	 	tripd2(d,e,f,n2-1,n1);
	    }

	 	for(i2=0; i2<n2-1; ++i2)
			for(i1=0; i1<n1; ++i1)
				v[i3][i2+1][i1] = f[i2][i1];
	}
	}
 
	if(r3>0.) {
/*	smooth velocity in  the third  direction */

	/* allocate space */
 	d = sf_floatalloc2(n1,n3);
	e = sf_floatalloc2(n1,n3);
	f = sf_floatalloc2(n1,n3); 
 
	for(i2=0; i2<n2; ++i2){
		if(depth==2) ww = w[i2];
	 	for(i3=0; i3<n3-1; ++i3){
			if(depth==3) ww = w[i3+1];
			for(i1=0; i1<n1; ++i1){
				if(depth==1) ww = w[i1];
				d[i3][i1] = ww+2.*r3;
				e[i3][i1] = -r3;
 				f[i3][i1] = ww*v[i3+1][i2][i1];
			}
 		}
			for(i1=0; i1<n1; ++i1){
	  		d[n3-2][i1] -= r3;
			f[0][i1] += r3*v[0][i2][i1];
  		}
	 	tripd2(d,e,f,n3-1,n1);

	    for(i=1; i<iter; ++i){
	 	for(i3=0; i3<n3-1; ++i3){
			if(depth==3) ww = w[i3+1];
			for(i1=0; i1<n1; ++i1){
				if(depth==1) ww = w[i1];
				d[i3][i1] = ww+2.*r3;
				e[i3][i1] = -r3;
 				f[i3][i1] *= ww;
			}
 		}
			for(i1=0; i1<n1; ++i1){
	  		d[n3-2][i1] -= r3;
			f[0][i1] += r3*v[0][i2][i1];
  		}
	 	tripd2(d,e,f,n3-1,n1);
	    }

	 	for(i3=0; i3<n3-1; ++i3)
			for(i1=0; i1<n1; ++i1)
				v[i3+1][i2][i1] = f[i3][i1];
	}
	}
	
	if(r1>0.) {
/*	smooth velocity in  the first direction */

	/* allocate space */
 	d = sf_floatalloc2(1,n1);
	e = sf_floatalloc2(1,n1);
	f = sf_floatalloc2(1,n1);
 
	for(i3=0; i3<n3; ++i3){
		if(depth==3) ww = w[i3];
	 	for(i2=0; i2<n2; ++i2){
			if(depth==2) ww = w[i2];
			for(i1=0; i1<n1-1; ++i1){
				if(depth==1) ww = w[i1+1];
				d[i1][0] = ww+r1*2.0;
				e[i1][0] = -r1;
 				f[i1][0] = ww*v[i3][i2][i1+1];
			}
	  		d[n1-2][0] -= r1;
			f[0][0] += r1*v[i3][i2][0];
	   		tripd2(d,e,f,n1-1,1);

		    for(i=1; i<iter; ++i) {
			for(i1=0; i1<n1-1; ++i1){
				if(depth==1) ww = w[i1+1];
				d[i1][0] = ww+r1*2.0;
				e[i1][0] = -r1;
 				f[i1][0] *= ww;
			}
	  		d[n1-2][0] -= r1;
			f[0][0] += r1*v[i3][i2][0];
	 		tripd2(d,e,f,n1-1,1);
		    }

 			for(i1=0; i1<n1-1; ++i1)
				v[i3][i2][i1+1] = f[i1][0];
		}
	}
	}

	if(sl) {
		for(i3=0; i3<n3; ++i3) 
			for(i2=0; i2<n2; ++i2)
				for(i1=0; i1<n1; ++i1)
					v[i3][i2][i1] = 1.0/v[i3][i2][i1];
	}

    free(w);
	if(r1>0. || r2>0. || r3>0.) {
        free(d);free(e);free(f);

 	}
}
	
	
void tripd2(float **d, float **e, float **b, int n, int m)
/*****************************************************************************
Given m n-by-n symmetric, tridiagonal, positive definite matri2 A's and m
n-vector b's, the following algorithm overwrites b with the solution to Ax = b.
The first dimension of arrays is independent of the algorithm. 

  d() the diagonal of A 
  e() the superdiagonal of A
*****************************************************************************/
{
	int k, i; 
	float temp;
	
	/* decomposition */
	for(k=1; k<n; ++k) 
		for(i=0; i<m; ++i){ 
	  		 temp = e[k-1][i];
	   		e[k-1][i] = temp/d[k-1][i];
	   d[k][i] -= temp*e[k-1][i];
	}

	/* substitution	*/
	for(k=1; k<n; ++k) 
		 for(i=0; i<m; ++i) 
 			b[k][i] -= e[k-1][i]*b[k-1][i];
	
	for(i=0; i<m; ++i) 
		b[n-1][i] /=d[n-1][i];

	for(k=n-1; k>0; --k) 
		 for(i=0; i<m; ++i) 
			 b[k-1][i] = b[k-1][i]/d[k-1][i]-e[k-1][i]*b[k][i]; 
	
}
void smooth(float ***vel3D,float *ds,int nx,int ny,int nz)
{
	int i,j,k,siren,v;
	float s1,d0,d1,d2,d3;
	for(i=0;i<nx*ny*nz;i++)ds[i]=ds[i]/1000;

		for(i=0;i<nx;i++)
			for(j=0;j<ny;j++)
				for(k=0;k<nz;k++)
				{
					if(vel3D[i][j][k]!=0)
					{
						s1=1./vel3D[i][j][k];
						if(ds[i+nx*j+nx*ny*k]>s1*0.5)ds[i+nx*j+nx*ny*k]=s1*0.5;
						if(ds[i+nx*j+nx*ny*k]<-s1*0.5)ds[i+nx*j+nx*ny*k]=-s1*0.5;
						vel3D[i][j][k]=1./(s1+ds[i+nx*j+nx*ny*k]);
					}
				}
		for(i=0;i<nx;i++)
			for(j=0;j<ny;j++)
				for(k=0;k<nz;k++)
				{		if(vel3D[i][j][k]>10)
                                        {
					v=0;siren=0;
					if(i-1>=0&&j-1>=0&&k-1>=0){v=v+vel3D[i-1][j-1][k-1];siren++;}
					if(j-1>=0&&k-1>=0){v=v+vel3D[i][j-1][k-1];siren++;}
					if(i+1<=nx-1&&j-1>=0&&k-1>=0){v=v+vel3D[i+1][j-1][k-1];siren++;}
					if(i-1>=0&&k-1>=0){v=v+vel3D[i-1][j][k-1];siren++;}
					if(k-1>=0){v=v+vel3D[i][j][k-1];siren++;}
					if(i+1<=nx-1&&k-1>=0){v=v+vel3D[i+1][j][k-1];siren++;}
					if(i-1>=0&&j+1<=ny-1&&k-1>=0){v=v+vel3D[i-1][j+1][k-1];siren++;}
					if(j+1<=ny-1&&k-1>=0){v=v+vel3D[i][j+1][k-1];siren++;}
					if(i+1<=nx-1&&j+1<=ny-1&&k-1>=0){v=v+vel3D[i+1][j+1][k-1];siren++;}

					if(i-1>=0&&j-1>=0){v=v+vel3D[i-1][j-1][k];siren++;}
					if(j-1>=0){v=v+vel3D[i][j-1][k];siren++;}
					if(i+1<=nx-1&&j-1>=0){v=v+vel3D[i+1][j-1][k];siren++;}
					if(i-1>=0){v=v+vel3D[i-1][j][k];siren++;}			
					if(i+1<=nx-1){v=v+vel3D[i+1][j][k];siren++;}
					if(i-1>=0&&j+1<=ny-1){v=v+vel3D[i-1][j+1][k];siren++;}
					if(j+1<=ny-1){v=v+vel3D[i][j+1][k];siren++;}
					if(i+1<=nx-1&&j+1<=ny-1){v=v+vel3D[i+1][j+1][k];siren++;}

					if(i-1>=0&&j-1>=0&&k+1<=nz-1){v=v+vel3D[i-1][j-1][k+1];siren++;}
					if(j-1>=0&&k+1<=nz-1){v=v+vel3D[i][j-1][k+1];siren++;}
					if(i+1<=nx-1&&j-1>=0&&k+1<=nz-1){v=v+vel3D[i+1][j-1][k+1];siren++;}
					if(i-1>=0&&k+1<=nz-1){v=v+vel3D[i-1][j][k+1];siren++;}
					if(k+1<=nz-1){v=v+vel3D[i][j][k+1];siren++;}
					if(i+1<=nx-1&&k+1<=nz-1){v=v+vel3D[i+1][j][k+1];siren++;}
					if(i-1>=0&&j+1<=ny-1&k+1<=nz-1){v=v+vel3D[i-1][j+1][k+1];siren++;}
					if(j+1<=ny-1&&k+1<=nz-1){v=v+vel3D[i][j+1][k+1];siren++;}
					if(i+1<=nx-1&&j+1<=ny-1&&k+1<=nz-1){v=v+vel3D[i+1][j+1][k+1];siren++;}
				
					vel3D[i][j][k]=1.0/(2*siren)*v+0.5*vel3D[i][j][k];
                       //    if(i%10==0&&j%10==0&&k%10==0)printf("%f \n",vel3D[i][j][k]);
                                   
				}
                             }

}
void smooth3(float ***vel3D,float ***vel_x3D,float ***vel_q3D,float ***eps,float ***deta,int nx,int ny,int nz)
{
 int i,j,k;
  for(i=0;i<nx;i++)
    for(j=0;j<ny;j++)
      for(k=0;k<nz;k++)
       {  eps[i][j][k]=sqrt(((vel_x3D[i][j][k]*vel_x3D[i][j][k])/(vel3D[i][j][k]*vel3D[i][j][k])-1)*((vel_x3D[i][j][k]*vel_x3D[i][j][k])/(vel3D[i][j][k]*vel3D[i][j][k])-1)/4);//problem
          deta[i][j][k]=sqrt(((2*eps[i][j][k]+1)*vel_q3D[i][j][k]-1)*((2*eps[i][j][k]+1)*vel_q3D[i][j][k]-1)/4);
         //  if(i%10==0&&j%10==0&&k%10==0)printf("%f %f %f %f\n",vel3D[i][j][k],vel_x3D[i][j][k],eps[i][j][k],deta[i][j][k]);
         }
}

