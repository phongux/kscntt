import sys
sys.path.insert(0, "F:/wsgi/kscntt")
from beaker.middleware import SessionMiddleware
import importlib
import re
import json
import config.module
from datetime import datetime
import config.sess
import config.conn
import config.login
from config.load import Load

importlib.reload(config.module)

def application(environment, start_response):
    from webob import Request, Response
    request = Request(environment)
    params = request.params
    post = request.POST
    login = config.login.Login()
    # Get the session object from the environ
    session = environment['beaker.session']
    if 'username' not in session:
        page = login.login_again()
    elif 'password' not in session:
        page = login.login_again()
    else:
        user = session['username']
        passwd = session['password']
        captcha = session['captcha']
        connect = config.conn.Connect(user=user, passwd=passwd, captcha=captcha)
        ps = connect.check_account()
        if ps[0][2] > 0:
            page = ""
            if 'display' not in post:
                display = 20
            else:
                display = post['display']
            if 'table' not in post:
                table = f'yeu_cau_{datetime.utcnow().year}'
            else:
                table = post['table']
            if 'hidecols' not in post:
                hidecols = []
            else:
                hidecols = post.getall('hidecols')
            module = config.module.Module(user=user, account_level=ps[0][2], table=table)
            table_names = module.get_table_name()
            head = module.head()
            headlink = module.headlink()
            menuadmin = module.menuadmin()
            menuuser = module.menuuser()
            menuhead = module.menuhead()
            menufoot = module.menufoot()
            save = module.save
            load = module.load
            rws = module.get_type_columns()
            cols = [desc[0] for desc in rws if desc[0] not in hidecols]
            load_all = Load(tablename='yeu_cau', columnname='kieu_yeu_cau')
            kieu_yeu_cau = [item[0] for item in load_all.get_value_option()]
            load_all.columnname='che_do'
            che_do = [item[0] for item in load_all.get_value_option()]
            load_all.columnname='cap_do'
            cap_do = [item[0] for item in load_all.get_value_option()]
            load_all.columnname='trang_thai'
            trang_thai = [item[0] for item in load_all.get_value_option()]
            load_all.columnname='nhom'
            nhom = [item[0] for item in load_all.get_value_option()]
            load_all.columnname='loai_dich_vu'
            loai_dich_vu = [item[0] for item in load_all.get_value_option()]
            nguoi_yeu_cau = [item[0] for item in load_all.get_nguoi_yeu_cau()]
            ky_thuat = [item[0] for item in load_all.get_ky_thuat()]
            type_config = {
                'account_password': {'type': 'password'},
                'account_level': {'type': 'numeric', 'allowEmpty': 'false'},
                'username': {'allowEmpty': 'false'},
                'fid': {'type': 'numeric', 'allowEmpty': 'false'},
                'ngay': {'type': 'date', 'dateFormat': 'YYYY-MM-DD', 'correctFormat': 'true',
                         'defaultDate': f'{str(datetime.today().date())}'},
                'kieu_yeu_cau':{'editor':'select', 'selectOptions': kieu_yeu_cau},
                'che_do': {'editor': 'select', 'selectOptions': che_do},
                'cap_do': {'editor': 'select', 'selectOptions': cap_do},
                'trang_thai': {'editor': 'select', 'selectOptions': trang_thai},
                'nhom': {'editor': 'select', 'selectOptions': nhom},
                'loai_dich_vu': {'editor': 'select', 'selectOptions': loai_dich_vu},
                'nguoi_yeu_cau': {'type': 'autocomplete', 'source': nguoi_yeu_cau},
                'ky_thuat': {'type': 'autocomplete', 'source': ky_thuat}
            }
            columns = []
            for colname in cols:
                if colname in type_config.keys():
                    columns.append(type_config.get(colname))
                else:
                    columns.append({})

            if ps[0][4] == 'kh':
                readonly = f"""hot.getDataAtCell(row,colu.indexOf('nguoi_yeu_cau')) != '{ps[0][0]}' && hot.getDataAtCell(row,colu.indexOf('nguoi_yeu_cau')) != null || col == colu.indexOf("ngay") || col == colu.indexOf("update_time") || col == colu.indexOf("nguoi_yeu_cau")|| col == colu.indexOf("huong_xu_ly") || col == colu.indexOf("id")"""
                minSpareRows = ''
                contextMenu = "['row_above','row_below','remove_row','undo','redo','alignment','cut','copy']"
            elif ps[0][4] == 'nv':
                readonly = f"""hot.getDataAtCell(row,colu.indexOf('ky_thuat')) != '{ps[0][0]}' && hot.getDataAtCell(row,colu.indexOf('ky_thuat')) != null || col == colu.indexOf("ngay") || col == colu.indexOf("update_time") || col == colu.indexOf("id") || col == colu.indexOf("y_kien_khach_hang")"""
                minSpareRows = "hot.updateSettings({minSpareRows:1});"
                contextMenu = "['row_above','row_below','undo','redo','alignment','cut','copy']"
            else:
                readonly = f"""col != 100"""
                minSpareRows = "hot.updateSettings({minSpareRows:1});"
                contextMenu = "['row_above','row_below','remove_row','undo','redo','alignment','cut','copy']"
            loadurl = f"""'{load}/load_control_user'"""
            saveurl = f"""'{save}/save_control_user'"""
            page += head
            page += "<title>Control</title>"
            page += headlink
            page += """
                </head>
                <body>"""
            page += menuhead
            if int(ps[0][2]) == 2:
                page += menuadmin
            else:
                page += menuuser
            page += menufoot
            # for in this case need add more filter duplicate row in table home;
            page += f"""
            <br />
            <br />
            <br />
            <p> Account : {user} , table: {table} </p>
            <br />
            <form method="post" action="">                              
                <div class="btn-group">
                    <label class='btn-group' >Table:
                        <input class='btn-group form-control' list="table" name="table" value=""  onchange='if(this.value != 0) {{ this.form.submit(); }}'>
                        <datalist id="table">"""
            for tablename in table_names:
                page += f"""<option value="{tablename[0]}">{tablename[0]}</option>"""
            page += f"""</datalist>
                    </label> 
                </div>
                <div class="btn-group">
                    <label class='btn-group' >Display:
                        <input class='btn-group col-sm-4 form-control' list="display" name="display" value="{display}">
                        <datalist id="display">
                            <option value="5">5</option>
                            <option value="10">10</option>
                            <option value="20">20</option>
                            <option value="40">40</option>                                    
                        </datalist>
                    </label> 
                </div>  
            </form>
            <div class="controls">
                <button name="load" id="load" class="intext-btn">Load</button>
                <button name="save" id="save" class="intext-btn">Save</button>
                <label><input type="checkbox" name="autosave" id="autosave" checked="checked" autocomplete="off">Autosave</label>
            </div>
            <div>
                <span class="page2">No page selected</span> |
                <strong>
                    <span id="exampleConsole" class="console">
                        Click "Load" to load data from server 
                    </span>
                </strong> 
            </div>
            <div id="example1" style="width:100%; height: 520px; overflow: hidden"></div>
            <nav class="demo2"></nav>
            <script>
                var $$ = function(id) {{
                    return document.getElementById(id);
                }},
                table = '{table}',
                colu = {cols},
                autoload=0,
                display = {display},
                page_number = 1,
                autosave = $$('autosave'),
                save = $$('save'),
                load = $$('load'),
                loadall = $$('loadall'),
                $container = $("#example1"),
                $console = $("#exampleConsole"),
                $parent = $container.parent(),
                autosaveNotification,
                hot;
                hot = new Handsontable($container[0], {{
                    columnSorting: true,
                    startRows: 1,
                    startCols: 3,
                    currentRowClassName: 'currentRow',
                    currentColClassName: 'currentCol',
                    autoWrapRow: true,
                    rowHeaders: true,
                    colHeaders: colu,
                    columns: {columns},
                    //colWidths: [50,250,250,250],        
                    manualColumnResize: true,
                    manualRowResize: true,      
                    autoColumnSize : true,
                    //stretchH: 'all',    
                    minSpareCols: 0,
                    minSpareRows: 0,
                    undo:true,
                    redo: true,
                    contextMenu: {contextMenu},
                    beforeRedo: function(action){{
                        if (!autosave.checked) {{
                            return;
                        }}
                        var insertundo =[];
                        if(action.actionType == 'remove_row'){{
                            var dellist = []
                            for (var i =0; i < action.data.length; i++){{
                                dellist.push(action.data[i][0]);
                            }}
                            $.ajax({{
                                url: {saveurl},
                                data: {{table: table,delete:dellist}}, // returns all cells' data
                                dataType: 'json',
                                type: 'POST',
                                success: function(res) {{
                                    if (res.result === 'ok') {{
                                        autosaveNotification = setTimeout(function () {{
                                            $console.text('Delete: '+ dellist.length +' | Changes will be autosaved ');
                                        }}, 500);
                                    }}
                                    else {{
                                        $console.text('Save error');
                                    }}
                                }},
                                error: function () {{
                                    $console.text('Save error');
                                }}
                            }});        
                        }}
                    }},
                    beforeUndo: function(action){{
                        if (!autosave.checked) {{
                            return;
                        }}
                        if(action.actionType == 'remove_row'){{
                        var insertundo =[];
                            for (var i=0; i< action.data.length; i++){{ 
                            var newrow = {{}};
                            for (var j =0; j < colu.length;j++){{
                                newrow[colu[j]] = action.data[i][j];
                            }}
                            insertundo.push(newrow);
                            }}
                            $.ajax({{
                                url: {saveurl},
                                dataType: 'json',
                                type: 'POST',
                                data: {{
                                    table:table,                                    
                                    insert:insertundo,
                                    lenundo:insertundo.length,
                                    cols: colu
                                }},
                                success: function (res) {{
                                    if (res.result === 'ok') {{
                                        var page_num = parseInt(document.getElementById("page_number").innerText);
                                        autosaveNotification = setTimeout(function () {{
                                            $console.text('Undo: '+insertundo.length + ' | Changes will be autosaved ');
                                        }}, 500);
                                    }}
                                    else{{
                                        $console.html("<font color='red'>Data save error</font>");}}
                                    }},
                                    error: function (res) {{
                                        autosaveNotification = setTimeout(function () {{
                                            $console.html("<font color='red'>Data save error:</font>");
                                        }},500);
                                    }}
                                }});
                            }}
                            else if(action.actionType == 'change'){{
                                var change;
                                change = action.changes;
                                var update = [],insert=[],rows=[],unique=[];
                                for (var i=0;i<change.length;i++){{
                                    if (hot.getData()[change[i][0]][colu.indexOf("id")] == null){{
                                        rows.push(change[i][0]);
                                    }}
                                    else{{
                                        update.push({{"id":hot.getData()[change[i][0]][colu.indexOf("id")],"column":colu[change[i][1]],"value":change[i][2]}});
                                    }}
                                }}
                                if (rows.length >0) {{  
                                    for(var i in rows){{
                                        if(unique.indexOf(rows[i]) === -1){{
                                            unique.push(rows[i]);
                                        }}
                                    }}                
                                }}
                                clearTimeout(autosaveNotification);
                                $.ajax({{
                                    url: {saveurl},
                                    dataType: 'json',
                                    type: 'POST',
                                    data: {{
                                        table:table,
                                        update:update,
                                        lenupdate:update.length,
                                        cols: colu
                                    }},
                                    success: function (res) {{
                                        if (res.result === 'ok') {{
                                            autosaveNotification = setTimeout(function () {{
                                                $console.text('Undo: '+update.length + ' | Changes will be autosaved ');
                                            }}, 500);
                                        }}
                                        else{{
                                            $console.html("<font color='red'>Data save error</font>");}}
                                        }},
                                        error: function (res) {{
                                            autosaveNotification = setTimeout(function () {{
                                            $console.html("<font color='red'>Data save error:</font>");
                                        }}, 
                                        500);
                                    }}
                                }});
    
                            }}
                        }},
                        beforeRemoveRow: function(index, amount) {{
                            var dellist=[];
                            for(var i=0; i<amount; i++){{
                                if (hot.getData()[index +i][colu.indexOf("id")] !=null){{
                                    dellist.push(hot.getData()[index +i][colu.indexOf("id")]);
                                }}
                            }}
                            if (!autosave.checked) {{
                                Handsontable.dom.addEvent(save, 'click', function() {{
                                    deleteRows(dellist);
                                }});
                                return;
                            }}
                            deleteRows(dellist);       
                        }},              
                        afterChange: function (change, source) {{
                            if (source === 'loadData'){{
                                return;                            
                            }}
                            if (source === 'UndoRedo.undo'){{
                                return;
                            }}
                            if (!autosave.checked) {{
                                return;
                            }}
                            if (change !=null){{
                            var update = [],insert=[],rows=[],unique=[];
                            for (var i=0;i<change.length;i++){{
                                if (hot.getData()[change[i][0]][colu.indexOf("id")] == null){{
                                    rows.push(change[i][0]);
                                }}
                                else{{
                                    update.push({{"id":hot.getData()[change[i][0]][colu.indexOf("id")],"column":colu[change[i][1]],"value":change[i][3]}});
                                }}
                            }}
                            if (rows.length >0) {{  
                                for(var i in rows){{
                                    if(unique.indexOf(rows[i]) === -1){{
                                        unique.push(rows[i]);
                                    }}
                                }}                
                                for (var i in unique){{
                                    var son = {{}};
                                    for (var k in colu){{
                                        son[colu[k]] = hot.getData()[unique[i]][k]
                                    }}
                                    insert.push(son);
                                }}
                            }}
                            // transform sorted row to original row
                            clearTimeout(autosaveNotification);
                            $.ajax({{
                                url: {saveurl},
                                dataType: 'json',
                                type: 'POST',
                                data: {{
                                    table:table,
                                    update:update,
                                    lenupdate:update.length,
                                    insert:insert,
                                    leninsert:insert.length,
                                    cols: colu
                                }},
                                success: function (res) {{
                                    if (res.result === 'ok') {{
                                        autosaveNotification = setTimeout(function () {{
                                            $console.text('Update: '+update.length + ' | Insert: ' + insert.length + ' | Changes will be autosaved ');
                                            if (insert.length > 0){{
                                                $("#load").click();
                                            }};
                                        }}, 500);
                                    }}
                                    else{{
                                        $console.html("<font color='red'>Data save error</font>");}}
                                    }},
                                    error: function (res) {{
                                        autosaveNotification = setTimeout(function () {{
                                        $console.html("<font color='red'>Data save error:</font>");
                                    }}, 
                                    500);
                                }}
                            }});
                            }}
                        }}
                    }});
     
                hot.selectCell(3,3);
                //hot.updateSettings({{columns: [{{data:1}},{{data:2,type:"password"}},{{data:3}},{{data:4}},{{data:5}},{{data:6}}] }});
                Handsontable.dom.addEvent(save, 'click', function() {{
                    // save all cell's data
                    var update = [],insert=[],rows=[],unique=[];
                    var data;
                    data = hot.getData();
                    for(var i=0; i< data.length; i++){{
                        if(data[i][0] === null){{
                            var newrow = {{}};
                            for (var j =0; j < colu.length;j++){{
                                newrow[colu[j]] = data[i][j];
                            }}
                            insert.push(newrow);  
                        }}else{{
                            var newrow = {{}};
                            console.log(data[i]);
                            for (var j =0; j < colu.length;j++){{
                                newrow[colu[j]] = data[i][j];
                            }}
                            update.push(newrow);                          
                        }}
                    }}
                    insert.length = insert.length-1;
                    $.ajax({{
                        url: {saveurl},
                        dataType: 'json',
                        type: 'POST',
                        data: {{
                            table:table,
                            insert:insert,
                            leninsert:insert.length,
                            updateall:update,
                            lenupdateall:update.length,
                            cols: colu
                        }},
                        success: function (res) {{
                            if (res.result === 'ok') {{
                                autosaveNotification = setTimeout(function () {{
                                    $console.text('Update: '+update.length + ' | Insert: ' + insert.length + ' | Changes will be saved ');
                                }}, 500);
                            }}
                            else{{
                                $console.html("<font color='red'>Data save error</font>");}}
                            }},
                            error: function (res) {{
                                autosaveNotification = setTimeout(function () {{
                                $console.html("<font color='red'>Data save error:</font>");
                            }}, 
                            500);
                        }}
                    }});    
                }});
    
                Handsontable.dom.addEvent(autosave, 'click', function() {{
                    if (autosave.checked) {{
                        exampleConsole.innerText = 'Changes will be autosaved';
                    }}
                    else {{
                        exampleConsole.innerText ='Changes will not be autosaved';
                    }}
                }});
                Handsontable.dom.addEvent(load, 'click', function() {{
                    if(document.getElementById('page_number')){{
                        page_number = parseInt(document.getElementById('page_number').innerText);  
                    }}
                    (async function(){{
                        await loadPage(page_number);
                    }})();
                }});
    
                function loadPage(page_number){{
                    return new Promise(function (resolve,reject){{
                            if(document.getElementById('page_number')){{
                                page_number = parseInt(document.getElementById('page_number').innerText);  
                            }}
                            $.ajax({{
                                url: {loadurl},
                                data: JSON.parse(
                                JSON.stringify({{
                                    "display":display,
                                    "page":page_number,
                                    "table":table,
                                    "cols":colu
                                }})
                            ),
                            dataType: 'json',
                            type: 'POST',                   
                            success: function (res) {{
                                var data = [], row;
                                for (var i = 0, ilen = res.product.length; i < ilen; i++) {{
                                    row = [];
                                    for(var m in colu){{
                                        row[m] = res.product[i][colu[m]];
                                    }}
                                    data[res.product[i].idha - 1] = row;
                                }}
                                $console.text('Data loaded');
                                    if(page_number== res.sum_page || res.sum_page == 0){{
                                        hot.updateSettings({{minSpareRows:1}});
                                    }}
                                    else{{
                                        hot.updateSettings({{minSpareRows:0}});
                                    }};                                
                                $(".page2").html("<strong>Page <span id='page_number'>"+page_number+"</span> / <span id='total_page'>" + Math.round(res.sum_page)+"</span></strong> | <strong><span id='total_rows'> Rows: " + Math.round(res.rows)+"</span></strong> | <strong><span id='total_rows'> Display: " + Math.round(res.display)+"</span></strong>");
                                hot.loadData(data);
                                resolve({{"page_number":page_number,"sum_page":Math.ceil(res.sum_page),"rows":Math.ceil(res.rows),"display":res.display}});
                            }}
                        }});
                    }});
                }}
                function pagination(res){{
                    return new Promise(function(resolve,reject){{
                    $('.demo2').bootpag({{
                        total: res.sum_page,
                                page: res.page_number,
                                maxVisible: 10,
                                //href:'../demo/account_manager.py?page={{{{number}}}}',
                                leaps: false,
                                firstLastUse: true,
                                first: '←',
                                last: '→',
                                wrapClass: 'pagination',
                                activeClass: 'active',
                                disabledClass: 'disabled',
                                nextClass: 'next',
                                prevClass: 'prev',
                                lastClass: 'last',
                                firstClass: 'first'
                                }}).on('page', function(event, num){{
                                    if(num == parseInt($("#total_page").text())){{
                                        hot.updateSettings({{minSpareRows:1}});
                                    }}
                                    else{{
                                        hot.updateSettings({{minSpareRows:0}});
                                    }};
                                    $(".page2").html("<strong>Page <span id='page_number'>"+num+"</span> / <span id='total_page'>" + Math.round(res.sum_page)+"</span></strong> | <strong><span id='total_rows'> Rows: " + Math.round(res.rows)+"</span></strong> | <strong><span id='rows_per_page'> Display: " + Math.round(res.display)+"</span></strong>");
                                    $.ajax({{
                                        url: {loadurl},
                                        data: JSON.parse(
                                        JSON.stringify({{
                                            table:table,
                                            cols:colu,
                                            "page":num,
                                            "display":display
                                        }})
                                    ),
                                    dataType: 'json',
                                    type: 'POST',
                                    success: function (res) {{
                                        var data = [], row;
                                        for (var i = 0, ilen = res.product.length; i < ilen; i++) {{
                                        row = [];
                                        for(var m in colu){{
                                            row[m] = res.product[i][colu[m]];
                                        }}
                                        data[res.product[i].idha - 1] = row;
                                    }}
                                    $console.text('Data loaded');
                                    hot.loadData(data);
                                    resolve();
                                }}
                            }});
                        }});  
                    }})
                }}
                function deleteRows(dellist){{
                    return new Promise(function(resolve, reject){{
                    $.ajax({{
                        url: {saveurl},
                        data: {{table:table, delete:dellist}}, // returns all cells' data
                        dataType: 'json',
                        type: 'POST',
                        success: function(res) {{
                            if (res.result === 'ok') {{
                                autosaveNotification = setTimeout(function () {{
                                    $console.text('Delete: '+ dellist.length +' | Changes will be saved ');
                                }}, 500);
                            }}
                            else {{
                                $console.text('Save error');
                            }}
                        }},
                        error: function () {{
                            $console.text('Save error');
                        }}
                            }});  
                    }});
                }}
                (async function(){{
                    res =  await loadPage(page_number);
                    await pagination(res);
                }})();
                hot.updateSettings({{cells: function(row, col, prop) {{
                        var cellProperties = {{}};
                            if ({readonly}) {{
                                cellProperties.readOnly = 'true'
                            }}
                        return cellProperties
                    }}}});
                </script>
            </body>
            </html>"""
        else:
            page = login.login_again()
    response = Response(body=page, content_type="text/html", charset="utf8", status="200 OK")
    return response(environment, start_response)

sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
