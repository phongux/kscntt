import sys
sys.path.insert(0,"F:/wsgi/kscntt")
import config.conn
import hashlib
import importlib
importlib.reload(config.conn)

class Module:

    def __init__(self, user=None, password=None, captcha=None, *args,**kwargs):
        self.project = "/wsgi/kscntt"
        self.control = f"/kscntt/control"
        self.js = f"/kscntt/js"
        self.bootstrap = f"/kscntt/bootstrap"
        self.load = f"{self.project}/load"
        self.save = f"{self.project}/save"
        self.user = user
        self.password = password
        self.captcha = captcha

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
        headlink = f"""<script type="text/javascript" src="{self.js}/jquery.js"></script>
        <script type="text/javascript" src="{self.bootstrap}/js/bootstrap.js"></script>
        <!--<script type="text/javascript" src="{self.bootstrap}/js/dropdowns-enhancement.js"></script>
        <script type="text/javascript" src="{self.bootstrap}/js/bootstrap-multiselect.js"></script>-->
        <link rel="stylesheet" href="{self.bootstrap}/css/bootstrap.css" type="text/css">
        <!--<link rel="stylesheet" href="{self.bootstrap}/css/dropdowns-enhancement.css" type="text/css">
        <link rel="stylesheet" href="{self.bootstrap}/css/bootstrap-multiselect.css" type="text/css"/>-->
        <script type="text/javascript" src="{self.js}/jquery.bootpag.min.js"></script>
        <script type="text/javascript" data-jsfiddle="common" src="{self.js}/handsontable.full.js"></script>
        <link data-jsfiddle="common" rel="stylesheet" media="screen" href="{self.js}/handsontable.full.css" type="text/css">
        <!-- the below is only needed for DateCell (uses jQuery UI Datepicker) -->
        <script type="text/javascript" src="{self.js}/jquery-ui.js"></script>
        <script type="text/javascript" scr="{self.js}/jquery-ui.js"></script>
        <link rel="stylesheet" href="{self.js}/jquery-ui.css" type="text/css">
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
                    $("#datepicker").datepicker();
                    $("#format").change(function() {{
                    $("#datepicker").datepicker( "option", "dateFormat", $( this ).val());
                    }});
                </script>"""
        return headlink

    def menuhead(self):
        menuhead = """<nav class="navbar navbar-expand-sm navbar-dark fixed-top bg-dark">
                            <ul class="navbar-nav">"""
        return menuhead
    def menufoot(self):
        menufoot = """</ul>
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
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown" href='{row_admin1[2]}' data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            {row_admin1[1]}
                            <b class="caret"></b>
                        </a>
                        <ul class="dropdown-menu">"""
                for row_admin2 in ps_admin_menu2:
                    menuadmin += f"""
                        <li class='dropdown-item'>
                            <a class='dropdown-item' href='{row_admin2[1]}'>
                                {row_admin2[0]}
                            </a>
                        </li>"""
                menuadmin += """</ul></li>"""
            else:
                menuadmin += f"""
                    <li class="nav-item">
                        <a class="nav-link" href='{row_admin1[2]}'>
                            {row_admin1[1]}
                        </a>
                    </li>"""
        for row1 in ps_menu1:
            if row1[0] == None:
                id2 = 0
            else:
                id2 = row1[0]
            cur.execute(f"""Select menu2,link from second_menu where first_menu_id = {id2} order by id """)
            ps_menu2 = cur.fetchall()
            if len(ps_menu2) > 0:
                menuadmin += f"""
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown" href='{row1[2]}'>
                            {row1[1]}
                            <b class="caret"></b>
                        </a>"""
                menuadmin += """<ul class="dropdown-menu">"""
                for row2 in ps_menu2:
                    menuadmin += f"""
                        <li class='dropdown-item'>
                            <a  class="dropdown-item" href='{row2[1]}'>
                                {row2[0]}
                            </a>
                        </li>"""
                menuadmin += """</ul></li>"""
            else:
                menuadmin += f"""
                    <li class="nav-item">
                        <a class="nav-link" href='{row1[2]}'>
                            {row1[1]}
                        </a>
                    </li>"""
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
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown" href='{row1[2]}' aria-haspopup="true" aria-expanded="false">
                            {row1[1]}
                            <b class="caret"></b>
                         </a>"""
                menuuser += """<ul class="dropdown-menu">"""
                for row2 in ps_menu2:
                    menuuser += f"""
                        <li class='dropdown-item'>
                            <a class="dropdown-item" href='{row2[1]}'>
                                {row2[0]}
                            </a>
                        </li>"""
                menuuser += """</ul></li>"""
            else:
                menuuser += f"""
                    <li class="nav-item" >
                        <a class="nav-link" href='{row1[2]}'>
                            {row1[1]}
                        </a>
                    </li>"""

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
            "select username,account_password,account_level,id from account where username=%s and account_password=%s ",
            (self.user, hashlib.sha512(self.password.encode('utf-8')).hexdigest(),))
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return ps


