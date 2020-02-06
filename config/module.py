import sys
sys.path.insert(0,"F:/wsgi/kscntt")
import config.conn
import hashlib
import importlib
importlib.reload(config.conn)

class Module:

    def __init__(self, user=None, password=None, account_level=None, captcha=None, account_menu=None, table=None, *args, **kwargs):
        self.project = "/wsgi/kscntt"
        self.control = f"/kscntt/control"
        self.js = f"/kscntt/js"
        self.bootstrap = f"/kscntt/bootstrap"
        self.dist = f"/kscntt/dist"
        self.load = f"{self.project}/load"
        self.save = f"{self.project}/save"
        self.user = user
        self.password = password
        self.captcha = captcha
        self.account_level = account_level
        self.account_menu = account_menu
        self.table = table

    def csshead(self):
        csshead = """
                  <style data-jsfiddle="common">
                    .handsontable .currentRow {
                      background-color: #E7E8EF;
                    }
                    .handsontable .currentCol {
                      background-color: #F9F9FB;
                    }
                    #ui-datepicker-div{z-index:9000;}
                    #datepicker{z-index:9000;}
                    #example1{z-index:1;}
                  </style>"""
        return csshead

    def head(self):
        head = """<!doctype html>
                    <html>
                        <head>
                            <meta charset='utf-8'>"""
        return head
    def csscheckbox(self):
        csscheckbox = """.multiselect-container>li>a>label {
          padding: 4px 20px 3px 20px;
        }"""
        return csscheckbox

    def headlink(self):
        headlink = f"""
        
        <link rel="shortcut icon" href="http://localhost/favicon2.ico" />
        <script type="text/javascript" src="{self.js}/jquery.js"></script>
        <script type="text/javascript" data-jsfiddle="common" src="{self.js}/handsontable.full.js"></script>
        <link data-jsfiddle="common" rel="stylesheet" media="screen" href="{self.js}/handsontable.full.css" type="text/css">
        <script type="text/javascript" src="{self.dist}/moment/moment.js"></script>
        <script type="text/javascript" src="{self.dist}/pikaday/pikaday.js"></script>
        <link rel="stylesheet" href="{self.dist}/pikaday/pikaday.css" type="text/css">
        <link rel="stylesheet" href="{self.bootstrap}/css/bootstrap.css" type="text/css">
        <script type="text/javascript" data-jsfiddle="common" src="{self.js}/popper.js"></script>
        <script type="text/javascript" src="{self.bootstrap}/js/bootstrap.js"></script>
        <!--<script type="text/javascript" src="{self.bootstrap}/js/dropdowns-enhancement.js"></script>
        <script type="text/javascript" src="{self.bootstrap}/js/bootstrap-multiselect.js"></script>-->
        <!--<link rel="stylesheet" href="{self.bootstrap}/css/dropdowns-enhancement.css" type="text/css">
        <link rel="stylesheet" href="{self.bootstrap}/css/bootstrap-multiselect.css" type="text/css"/>-->
        <script type="text/javascript" src="{self.js}/jquery.bootpag.min.js"></script>
        <!-- the below is only needed for DateCell (uses jQuery UI Datepicker)
        <script type="text/javascript" src="{self.js}/jquery-ui.js"></script>
        <link rel="stylesheet" href="{self.js}/jquery-ui.css" type="text/css">--> 
                    <style data-jsfiddle="common">
                    .handsontable .currentRow {{
                    background-color: #E7E8EF;
                    }}
        
                    .handsontable .currentCol {{
                    background-color: #F9F9FB;
                    }}
                    #ui-datepicker-div{{z-index:9000;}}
                    #datepicker{{z-index:9000;}}
                    #example1{{z-index:1;}}
                    </style>
                <script>
                    /*$("#datepicker").datepicker();
                    $("#format").change(function() {{
                    $("#datepicker").datepicker( "option", "dateFormat", $( this ).val());
                    }});*/
                </script>"""
        return headlink

    def summernote(self):
        summernote = f"""
            <link data-jsfiddle="common" rel="stylesheet" media="screen" href="{self.js}/summernote.css" type="text/css">
            <script type="text/javascript" data-jsfiddle="common" src="{self.js}/summernote.js"></script>
            <link data-jsfiddle="common" rel="stylesheet" media="screen" href="{self.js}/summernote-bs4.css" type="text/css">
            <script type="text/javascript" data-jsfiddle="common" src="{self.js}/summernote-bs4.js"></script>            

        """
        return summernote

    def menuhead(self):
        menuhead = """
        
        <nav class="navbar navbar-expand-sm navbar-dark fixed-top bg-dark">
            <img src="/kscntt/images/vsa_icon.png" style="width:3%;height:auto;" />
                            """
        return menuhead

    def menufoot(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(
            f"select menu1,link from account_menu order by fid")
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        menufoot = f"""
            <div class="nav ml-auto w-100 justify-content-end">
                <a class="nav-link dropdown-toggle" data-toggle="dropdown" href='' aria-haspopup="true" aria-expanded="false">
                    <b class="caret"></b>
                    {self.user}
                </a>
                <div class="dropdown-menu dropdown-menu-right">"""
        for item in ps:
            menufoot += f"""<a class="dropdown-item nav-link" href="{item[1]}">{item[0]}</a>"""
        menufoot += """
                </div>
            </div>
            </nav>"""
        return menufoot

    def menuadmin(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        menuadmin = ""
        cur.execute("""Select fid,menu1,link from admin_first_menu order by id""")
        ps_admin_menu1 = cur.fetchall()
        cur.execute("""Select fid,menu1,link from first_menu order by id""")
        ps_menu1 = cur.fetchall()

        for row_admin1 in ps_admin_menu1:
            if row_admin1[0] == None:
                id = 0
            else:
                id = row_admin1[0]
            cur.execute(f"""Select menu2,link from admin_second_menu where first_menu_id = {id} order by id """)
            ps_admin_menu2 = cur.fetchall()
            if len(ps_admin_menu2) > 0:
                menuadmin += f"""
                    <div class="dropdown">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown" href='{row_admin1[2]}' data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            {row_admin1[1]}
                            <b class="caret"></b>
                        </a>
                        <div class="dropdown-menu">"""
                for row_admin2 in ps_admin_menu2:
                    menuadmin += f"""
                            <a class='dropdown-item' href='{row_admin2[1]}'>
                                {row_admin2[0]}
                            </a>
                            """
                menuadmin += """</div></div>"""
            else:
                menuadmin += f"""
                    <div class="nav-item">
                        <a class="nav-link" href='{row_admin1[2]}'>
                            {row_admin1[1]}
                        </a>
                    </div>"""
        for row1 in ps_menu1:
            if row1[0] == None:
                id2 = 0
            else:
                id2 = row1[0]
            cur.execute(f"""Select menu2,link from second_menu where first_menu_id = {id2} order by id """)
            ps_menu2 = cur.fetchall()
            if len(ps_menu2) > 0:
                menuadmin += f"""
                    <div class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown" href='{row1[2]}'>
                            {row1[1]}
                            <b class="caret"></b>
                        </a>"""
                menuadmin += """<div class="dropdown-menu">"""
                for row2 in ps_menu2:
                    menuadmin += f"""
                            <a  class="dropdown-item" href='{row2[1]}'>
                                {row2[0]}
                            </a>
                            """
                menuadmin += """</div></div>"""
            else:
                menuadmin += f"""
                    <div class="nav-item dropdown">
                        <a class="nav-link" href='{row1[2]}'>
                            {row1[1]}
                        </a>
                    </div>
                        """
        con.commit()
        cur.close()
        con.close()
        return menuadmin


    def menuuser(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        menuuser = ""
        cur.execute("""Select fid,menu1,link from first_menu order by id""")
        ps_menu1 = cur.fetchall()
        for row1 in ps_menu1:
            if row1[0] == None:
                id3 = 0
            else:
                id3 = row1[0]
            cur.execute(f"""Select menu2,link from second_menu where first_menu_id = {id3} order by id """)
            ps_menu2 = cur.fetchall()
            if len(ps_menu2) > 0:
                menuuser += f"""
                    <div class="dropdown">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown" href='{row1[2]}' aria-haspopup="true" aria-expanded="false">
                            {row1[1]}
                            <b class="caret"></b>
                         </a>"""
                menuuser += """<div class="dropdown-menu">"""
                for row2 in ps_menu2:
                    menuuser += f"""
                            <a class="dropdown-item" href='{row2[1]}'>
                                {row2[0]}
                            </a>
                            """
                menuuser += """</div></div>"""
            else:
                menuuser += f"""
                    <div class="dropdown-menu">
                        <a class="nav-link" href='{row1[2]}'>
                            {row1[1]}
                        </a>
                    </div>
                        """

        con.commit()
        cur.close()
        con.close()
        return menuuser

    def update_captcha(self):
        connect = config.conn.Connect()
        conn = connect.get_connection()
        cur = conn.cursor()
        cur.execute("update account set captcha=%s where username=%s and account_password=%s", (self.captcha, self.user, hashlib.sha512(self.password.encode('utf-8')).hexdigest()))
        conn.commit()
        cur.close()
        conn.close()


    def get_account(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(
            "select username, account_password, account_level,team, account_group, id from account where username=%s and account_password=%s ",
            (self.user, self.password,))
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return ps

    def get_table_name(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(
            f"select tablename, account_level from settings where account_level<={self.account_level}")
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return ps

    def get_account_menu(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(
            f"select menu1,link from account_menu order by fid")
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return ps

    def get_table_account_level(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(
            f"select account_level from settings where tablename ='{self.table}'")
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return ps

    def get_type_columns(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(
            f"select column_name, data_type from information_schema.columns where table_name = '{self.table}'")
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return rows