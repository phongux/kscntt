# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, "F:/wsgi/kscntt")
from beaker.middleware import SessionMiddleware
import json
import importlib
import config.sess
import config.login
import config.conn
import config.module
from config.load import Load
importlib.reload(config.conn)
importlib.reload(config.module)

def application(environ, start_response):
    from webob import Response, Request
    request = Request(environ)
    post = request.POST
    params = request.params
    page = ""
    # Get the session object from the environ
    session = environ['beaker.session']
    login = config.login.Login()

    #Check to see if a value is in the session
    if not 'username' in session:
        page = login.login_again()
    elif not 'password' in session:
        page = login.login_again()
    else:
        user = session['username']
        passwd = session['password']
        captcha = session['captcha']
        module = config.module.Module(user=user, password=passwd)
        ps = module.get_account()

        if len(ps) == 0:
            page = login.login_again()
        else:
            module = config.module.Module(user=user)
            head = module.head()
            menuadmin = module.menuadmin()
            menuuser = module.menuuser()
            menuhead = module.menuhead()
            menufoot = module.menufoot()
            id = params.get('id')
            table = params.get('table')
            con = config.conn.Connect()
            con.sql = f"select kieu_yeu_cau,cap_do,che_do,trang_thai,nguoi_yeu_cau,nhom,ky_thuat, loai_dich_vu,chu_de ,mo_ta, file_path, huong_xu_ly,y_kien_khach_hang,id from {table} where id={id}"
            row = con.get_execute()
            row_kieu_yeu_cau = row[0]
            row_cap_do = row[1]
            row_che_do = row[2]
            row_trang_thai = row[3]
            row_nguoi_yeu_cau = row[4]
            row_nhom = row[5]
            row_ky_thuat = row[6]
            row_loai_dich_vu = row[7]
            row_chu_de = row[8]
            row_mo_ta = row[9]
            links = os.path.normpath(f"c:/Apache24/htdocs/kscntt/files/{row[10]}/")
            if links != os.path.normpath(f"c:/Apache24/htdocs/kscntt/files/None/"):
                files_name = os.listdir(links)
                link_down = [f"/kscntt/files/{row[10]}/{item}" for item in files_name]
                old_path = row[10]
            else:
                old_path = ''
                link_down = []

            row_huong_xu_ly = row[11]
            if row[12] is None:
                row_y_kien_khach_hang = ''
            else:
                row_y_kien_khach_hang = row[12]
            id = row[13]
            load_all = Load(tablename='yeu_cau', columnname='kieu_yeu_cau')
            load_all.selected = [row_kieu_yeu_cau]
            kieu_yeu_cau = load_all.get_option_select()
            load_all.selected = [row_che_do]
            load_all.columnname = 'che_do'
            che_do = load_all.get_option_select()
            load_all.selected = [row_cap_do]
            load_all.columnname = 'cap_do'
            cap_do = load_all.get_option_select()
            load_all.selected = [row_trang_thai]
            load_all.columnname = 'trang_thai'
            trang_thai = load_all.get_option_select()
            load_all.selected = [row_nhom]
            load_all.columnname = 'nhom'
            nhom = load_all.get_option_select()
            load_all.selected = [row_loai_dich_vu]
            load_all.columnname = 'loai_dich_vu'
            loai_dich_vu = load_all.get_option_select()
            list_nguoi_yeu_cau = [item[0].strip() for item in load_all.get_nguoi_yeu_cau()]
            load_all.option_select = list_nguoi_yeu_cau
            load_all.selected = [row_nguoi_yeu_cau]
            nguoi_yeu_cau = load_all.convert_option()
            load_all.option_select = list_nguoi_yeu_cau
            list_ky_thuat = [item[0].strip() for item in load_all.get_ky_thuat()]
            load_all.option_select = list_ky_thuat
            load_all.selected = row_ky_thuat
            ky_thuat = load_all.convert_option()
            load_all.link = link_down
            link = load_all.convert_link()
            page = ""
            page += head
            page += f"""
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
                <title>Edit request </title>
                <!-- include jquery -->
                <script src="//localhost/kscntt/js/jquery.js"></script>
                <!-- include libs stylesheets-->
                <link rel="stylesheet" href="//localhost/kscntt/bootstrap/css/bootstrap.css">
                <script src="//cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.js"></script>
                <script src="//localhost/kscntt/bootstrap/js/bootstrap.js"></script>
                <!-- include summernote -->
                <link rel="stylesheet" href="//localhost/kscntt/js/summernote-bs4.css">
                <script type="text/javascript" src="//localhost/kscntt/js/summernote-bs4.js"></script>
                <link href="https://cdn.jsdelivr.net/npm/select2@4.0.13/dist/css/select2.min.css" rel="stylesheet" />
                <script src="https://cdn.jsdelivr.net/npm/select2@4.0.13/dist/js/select2.min.js"></script>   
                <!--<link rel="stylesheet" href="examples/example.css">-->
                <script>
                    $(document).ready(function() {{
                        $('.js-example-basic-multiple').select2();
                    }});
                    $(document).ready(function() {{
                        $('.summernote').summernote();
                    }});
                </script>
            </head>
            """
            page += \
                """
                    <body>
                """
            page += menuhead
            if int(ps[0][2]) == 2:
                page += menuadmin
            else:
                page += menuuser
            page += menufoot
            page += """
            <br />
            <br />
            <br />
            <br />"""

            page += f"""<p><strong>Sửa yêu cầu </strong></p>
                <form method="post" action="../save/save_edit_request_detail" enctype="multipart/form-data">
                    <div class="form-row">
                        <div class="form-group col-md-6">
                            <label for="inputKieuYeuCau">Kiểu yêu cầu</label>
                            <select id="inputKieuYeuCau" class="form-control" name='kieu_yeu_cau'>
                                {kieu_yeu_cau}
                            </select>
                        </div>
                        <div class="form-group col-md-6">
                            <label for="inputCapDo">Cấp độ</label>
                            <select id="inputCapDo" class="form-control" name='cap_do'>
                                {cap_do}
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group col-md-6">
                            <label for="inputCheDo">Chế độ</label>
                            <select id="inputCheDo" class="form-control" name='che_do'>
                                {che_do}
                            </select>
                        </div>
                        <div class="form-group col-md-6">
                            <label for="inputTrangThai">Trạng Thái</label>
                            <select id="inputTrangThai" class="form-control" name='trang_thai'>
                                {trang_thai}
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group col-md-6">
                            <label for="inputNguoiYeuCau">Người Yêu Cầu</label>
                            <input class='form-control' list="nguoiYeuCau" name="nguoi_yeu_cau" value="{row_nguoi_yeu_cau}" />
                            <datalist id="nguoiYeuCau">
                                {nguoi_yeu_cau}
    `                       </datalist>
                        </div>
                        <div class="form-group col-md-6">
                            <label for="inputNhom">Nhóm</label>
                            <select id="inputNhom" class="form-control" name='nhom' value="{row_nhom}">
                                {nhom}
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group col-md-6">
                            <label for="inputKyThuat">Kỹ Thuật</label>
                            <select id='ky_thuat' class="form-control js-example-basic-multiple " name="ky_thuat" multiple="multiple">
                                {ky_thuat}
                            </select>
                        </div>
                        <div class="form-group col-md-6">
                            <label for="inputLoaiDichVu">Loại dịch vụ</label>
                            <select id="inputLoaiDichVu" class="form-control" name='loai_dich_vu'>
                                {loai_dich_vu}
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="inputChuDe">Chủ đề</label>
                        <input type="text" class="form-control" id="inputChuDe" name="chu_de" value="{row_chu_de}">
                    </div>
                    <div class="form-group">
                        <label for="inputMoTa">Mô tả</label>
                        <textarea class="summernote" name="mo_ta">{row_mo_ta}</textarea>
                    </div> 
                    <div class="form-group">
                        <label for="inputUpload">Các phần đính kèm</label>
                        <div>{link}</div>
                        <input type="file" class="form-control" name='file_dinh_kem' multiple>
                    </div>
                    <div class="form-group">
                        <label for="inputHuongXuLy">Hướng xử lý</label>
                        <textarea class="summernote" name="huong_xu_ly">{row_huong_xu_ly}</textarea>
                    </div>
                    <div class="form-group">
                        <label for="inputHuongXuLy">Ý kiến khách hàng</label>
                        <textarea class="summernote" name="y_kien_khach_hang">{row_y_kien_khach_hang}</textarea>
                    </div>
                    <input type='hidden' name='id' value='{id}' />
                    <input type='hidden' name='table' value='{table}' />
                    <input type='hidden' name='old_path' value='{old_path}' />
                    <button type="submit" class="btn btn-primary">Save</button>
                </form>
                <style>
                    input:focus, textarea:focus, select:focus{{
                        outline: none;
                    }}
                </style>    
            """

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environ, start_response)

# Configure the SessionMiddleware
sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
