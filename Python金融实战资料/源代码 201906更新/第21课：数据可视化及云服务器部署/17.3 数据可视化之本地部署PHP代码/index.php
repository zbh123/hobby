<!DOCTYPE html>
<html>

<head>
	<meta charset="utf-8">
	<title>华小智舆情监控系统</title>
	<style>
		table {margin:auto;border-collapse: collapse;width:90%;}
		table th {border: 1px solid #729EA5; padding: 8px; background-color:#ACC8CC;font-family:微软雅黑;text-align:center}
		table td {border: 1px solid #729EA5; padding: 8px; font-family:微软雅黑;text-align:center;background-color:#FFFFFF;opacity:0.9;}
		body {background-repeat:no-repeat;background-attachment:fixed;background-size: 100%;}
	</style>
</head>

<body background="背景.jpg">
	<p style="font-family:幼圆; color:white; font-size:26px; text-align:center">华小智舆情监控系统</p>
	<?php
	@$db = mysql_connect("localhost","root",""); //连接数据库服务
	@mysql_select_db("pachong3"); //连接具体的数据库

	$sql = "set names utf8"; //防止中文乱码，注意这里是utf8而不是utf-8
	mysql_query($sql); 


	//制作表格
	echo "<br>";
	echo "<table>";
		echo "<tr>"; //编写表头
			echo "<th>项目公司</th><th>主流网站信息</th><th>当日评分</th>";
		echo "</tr>";
		$companys = array("阿里巴巴","百度集团","华能信托","京东"); 
		foreach ($companys as $company)
		{
			$current_date = date("Y-m-d"); //当前日期(为2019-01-23的格式)
			$sql = "select * from test where company = '$company' and date = '$current_date' and score < 0";
			$result = mysql_query($sql);
			echo "<tr>"; 	
				echo "<td>$company</td>";   //填写项目公司
				echo "<td style='text-align:left'>"; //填写新闻信息
					echo "<ol>";
						$daily_score = 100;
						while($data = mysql_fetch_array($result)) 
						{
							$daily_score = $daily_score + $data[5];
							echo "<li><a href = $data[2] target='_blank'>$data[1]</a></li>";
						}
					echo "</ol>";
				echo "</td>";
				echo "<td>$daily_score</td>"; //填写评分
			echo "</tr>";
		}
	echo "</table>";
	echo "<br><br>";
	?>
</body>

</html>