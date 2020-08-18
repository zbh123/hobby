sql = """CREATE TABLE wind_dcm_without_gb (
         organization CHAR(150) NOT NULL,
         total_amount CHAR(150),
         total_ranking CHAR(150), 
         market_share CHAR(150),
         number CHAR(150),
         average_amount CHAR(150),
         remark CHAR(150),
         amount_npfb CHAR(150),
         market_share_npfb CHAR(150),
         number_npfb CHAR(150),
         amount_ed CHAR(150),
         market_share_ed CHAR(150),
         number_ed CHAR(150),
         amount_cd CHAR(150),
         market_share_cd CHAR(150),
         number_cd CHAR(150),
         amount_stfb CHAR(150),
         market_share_stfb CHAR(150),
         number_stfb CHAR(150),
         amount_mtn CHAR(150),
         market_share_mtn CHAR(150),
         number_mtn CHAR(150),
         amount_ot CHAR(150),
         market_share_ot CHAR(150),
         number_ot CHAR(150),
         amount_iad CHAR(150),
         market_share_iad CHAR(150),
         number_iad CHAR(150),
         amount_gbib CHAR(150),
         market_share_gbib CHAR(150),
         number_gbib CHAR(150),
         amount_abs CHAR(150),
         market_share_abs CHAR(150),
         number_abs CHAR(150),
         amount_exd CHAR(150),
         market_share_exd CHAR(150),
         number_exd CHAR(150),
         amount_other CHAR(150),
         market_share_other CHAR(150),
         number_other CHAR(150))
         "(organization, total_amount, total_ranking, market_share, number, " \
                                                "average_amount, remark, amount_npfb, market_share_npfb, number_npfb," \
                                                "amount_ed, market_share_ed, number_ed, amount_cd, market_share_cd," \
                                                "number_cd, amount_stfb, market_share_stfb, number_stfb, amount_mtn," \
                                                "market_share_mtn, number_mtn, amount_ot, market_share_ot, number_ot," \
                                                "amount_iad, market_share_iad, number_iad, amount_gbib, " \
                                                "market_share_gbib, number_gbib, amount_abs, market_share_abs, number_abs," \
                                                "amount_exd, market_share_exd, number_exd, amount_other," \
                                                "market_share_other, number_other, `current_time`) " \
                                                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                                "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                                                " %s, %s, %s, %s, %s, %s, %s, %s)" """

sql = """CREATE TABLE wind_dcm (
     organization CHAR(150) NOT NULL,
     total_amount CHAR(150),
     total_ranking CHAR(150), 
     market_share CHAR(150),
     number CHAR(150),
     average_amount CHAR(150),
     remark CHAR(150),
     amount_lgd CHAR(150),
     market_share_lgd CHAR(150),
     number_lgd CHAR(150),
     amount_pbd CHAR(150),
     market_share_pbd CHAR(150),
     number_pbd CHAR(150),
     amount_npfb CHAR(150),
     market_share_npfb CHAR(150),
     number_npfb CHAR(150),
     amount_ed CHAR(150),
     market_share_ed CHAR(150),
     number_ed CHAR(150),
     amount_cd CHAR(150),
     market_share_cd CHAR(150),
     number_cd CHAR(150),
     amount_stfb CHAR(150),
     market_share_stfb CHAR(150),
     number_stfb CHAR(150),
     amount_mtn CHAR(150),
     market_share_mtn CHAR(150),
     number_mtn CHAR(150),
     amount_ot CHAR(150),
     market_share_ot CHAR(150),
     number_ot CHAR(150),
     amount_iad CHAR(150),
     market_share_iad CHAR(150),
     number_iad CHAR(150),
     amount_gbib CHAR(150),
     market_share_gbib CHAR(150),
     number_gbib CHAR(150),
     amount_abs CHAR(150),
     market_share_abs CHAR(150),
     number_abs CHAR(150),
     amount_exd CHAR(150),
     market_share_exd CHAR(150),
     number_exd CHAR(150),
     amount_other CHAR(150),
     market_share_other CHAR(150),
     number_other CHAR(150))"""
# 去重
sql = "INSERT INTO " + table_name + " (`organization`, total_amount, total_ranking, market_share, `number`," \
                                                    "average_amount, remark, amount_lgd, market_share_lgd, number_lgd," \
                                                    "amount_pbd, market_share_pbd, number_pbd, amount_npfb," \
                                                    "market_share_npfb, number_npfb, amount_ed, market_share_ed, number_ed," \
                                                    "amount_cd, market_share_cd, number_cd, amount_stfb, market_share_stfb," \
                                                    "number_stfb, amount_mtn, market_share_mtn, number_mtn, amount_ot, " \
                                                    "market_share_ot, number_ot, amount_iad, market_share_iad, number_iad," \
                                                    "amount_gbib, market_share_gbib, number_gbib, amount_abs, " \
                                                    "market_share_abs, number_abs, amount_exd, market_share_exd, number_exd," \
                                                    "amount_other, market_share_other, number_other, `current_time`) " \
                                                   "SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                                                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                                                    " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
                                                   " FROM DUAL WHERE NOT EXISTS(SELECT `organization` FROM " + table_name + " WHERE `current_time` = '" + now_time + "')"

sql = """CREATE TABLE wind_ecm_list (
         organization_full CHAR(150),
         organization_abbr CHAR(150),
         total_fund	CHAR(150),
         ipo_fund CHAR(150),
         increase_under_fund CHAR(150),
         increase_finance_fund CHAR(150),
         issue_fund	CHAR(150),
         preferred_fund	CHAR(150),
         convertible_fund CHAR(150),
         total_underw CHAR(150),
         ipo_underw	CHAR(150),
         increase_under_underw CHAR(150),
         increase_finance_underw CHAR(150),
         issue_underw CHAR(150),
         preferred_underw CHAR(150),
         convertible_underw	CHAR(150),
         total_issue CHAR(150),
         ipo_issue CHAR(150),
         increase_under_issue CHAR(150),
         increase_finance_issue	CHAR(150),
         issue_issue CHAR(150),
         preferred_issue CHAR(150),
         convertible_issue CHAR(150)
        )"""

sql = """CREATE TABLE wind_ecm_issue (
         organization_full CHAR(150),
         organization_abbr CHAR(150),
         total_fund	CHAR(150),
         ipo_fund CHAR(150),
         increase_under_fund CHAR(150),
         increase_finance_fund CHAR(150),
         issue_fund	CHAR(150),
         preferred_fund	CHAR(150),
         convertible_fund CHAR(150),
         total_underw CHAR(150),
         ipo_underw	CHAR(150),
         increase_under_underw CHAR(150),
         increase_finance_underw CHAR(150),
         issue_underw CHAR(150),
         preferred_underw CHAR(150),
         convertible_underw	CHAR(150),
         total_issue CHAR(150),
         ipo_issue CHAR(150),
         increase_under_issue CHAR(150),
         increase_finance_issue	CHAR(150),
         issue_issue CHAR(150),
         preferred_issue CHAR(150),
         convertible_issue CHAR(150)
        )"""

sql = """CREATE TABLE wind_star (
         code CHAR(150),
         bond_abbr CHAR(150),
         announce_date_late	CHAR(150),
         enterprise	CHAR(150),
         audit_status CHAR(150),
         pre_disclosed CHAR(150),
         listing_board CHAR(150),
         ipo_theme CHAR(150),
         ipo_theme_detail CHAR(150),
         industry_csrc CHAR(150),
         pre_issued	CHAR(150),
         pre_total CHAR(150),
         place_registration	CHAR(150),
         sponsor CHAR(150),
         sponsor_person	CHAR(150),
         account_firm CHAR(150),
         accountant	CHAR(150),
         law_firm CHAR(150),
         lawyer	CHAR(150),
         change_status CHAR(150),
         announcement_date_f CHAR(150),
         website CHAR(150),
         email CHAR(150),
         phone CHAR(150),
         address CHAR(150)
        )"""

sql = """CREATE TABLE csrc_ipo (
     index_l CHAR(150),
     enterprise	CHAR(150),
     sponsor CHAR(150),
     account_firm CHAR(150),
     law_firm CHAR(150),
     accept_date CHAR(150),
     audit_status CHAR(150),
     spot_check	CHAR(150),
     remark CHAR(150)
    )"""

sql = """CREATE TABLE csrc_refinance (
     index_l CHAR(150),
     application_type CHAR(150),
     enterprise	CHAR(150),
     stock_code	CHAR(150),
     sponsor CHAR(150),
     accept_date CHAR(150),
     audit_status CHAR(150),
     remark CHAR(150)
    )"""

sql = """CREATE TABLE shenzhen_ipo (
      index_l CHAR(150),
      fullname_issuer CHAR(150),
      audit_status CHAR(150),
      place_registrate CHAR(150),
      srci CHAR(150),
      sponsor CHAR(150),
      law_firm CHAR(150),
      account_firm CHAR(150),
      update_date CHAR(150),
      accept_date CHAR(150)
     )"""

sql = """CREATE TABLE shenzhen_refinance (
     index_l CHAR(150),
     company CHAR(150),
     issuing_object	CHAR(150),
     finance_type CHAR(150),
     audit_status CHAR(150),
     srci CHAR(150),
     sponsor CHAR(150),
     law_firm CHAR(150),
     account_firm CHAR(150),
     update_date CHAR(150),
     accept_date CHAR(150)

    )"""
