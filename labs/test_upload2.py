import cgi, os, sys
from datetime import datetime
from webob import Request, Response
import uuid
import psycopg2
import psycopg2.extras
import psycopg2.extensions

def application(environ, start_response):
    request = Request(environ)
    s = str(uuid.uuid4())
    conn = psycopg2.connect("dbname=kscntt user=postgres host=localhost password=12345678 port=5432")
    cur = conn.cursor()
    # params = request.params
    try:  # Windows needs stdio set for binary mode.
        import msvcrt
        msvcrt.setmode(0, os.O_BINARY)  # stdin  = 0
        msvcrt.setmode(1, os.O_BINARY)  # stdout = 1
    except ImportError:
        pass

    def fbuffer(f, chunk_size=100000):
        while True:
            chunk = f.read(chunk_size)
            if not chunk: break
            # page = chunk

    if environ['REQUEST_METHOD'] == 'POST':
        # post = cgi.FieldStorage(
        #	fp=environ['wsgi.input'],
        #	environ=environ,
        #	keep_blank_values=True
        # )
        post = request.POST
        fileitem = post['file']
        account = 'test'
        table_name = 'hello'
        # account = request.headers["account"]  # .replace("A","")
        # time = request.headers["time"]
        # table_name = time.replace(" ", "_").replace(":", "_") + s
        # year = table_name.split("_")[3]
        # day = int(table_name.split("_")[2])
        # month = int(datetime.strptime(time, '%a %b %d %Y %H:%M:%S').month)
        year = datetime.today().year
        month = datetime.today().month
        day = datetime.today().day
        page = ""
        # dir = '/tmp/file_upload/%s%s%s%s/'%(account,year,month,day)
        # yf = f"""c:\tmp\file_upload\{year}"""
        # if not os.path.exists(yf):
        #     os.mkdir(yf)
        # ym = f"""c:\\tmp\\file_upload\\%s\\%s_%s""" % (year, year, month)
        # if not os.path.exists(ym):
        #     os.mkdir(ym)
        # yd = f"""c:\\tmp\\file_upload\\%s\\%s_%s\\%s_%s_%s""" % (year, year, month, year, month, day)
        # if not os.path.exists(yd):
        #     os.mkdir(yd)
        dir = r"""C:\Apache24\htdocs\kscntt\files"""

        if 'file' in post:
            filefield = post.getall('file')
            if not isinstance(filefield, list):
                filefield = [filefield]
            for fileitem in filefield:
                # #account = request.headers["account"]
                # #time = request.headers["time"]
                if fileitem.filename:

                    # strip leading path from file name to avoid directory traversal attacks
                    fn = os.path.basename(fileitem.filename)
                    open(dir + fn, 'wb').write(fileitem.file.read())

#                     cur.execute("""create table if not exists omnivore_%s_%s_%s
# 								(id serial8 primary key,no text,
# agent text, module text,domain text,title text,link text, quest text, answer text, time timestamp,process_time numeric,img_id text,
# 								update_time timestamp default now() )""" % (year, month, day))
#
#                     try:
#                         cur.copy_expert(
#                             """copy omnivore_%s_%s_%s(agent , module ,domain ,title ,link , quest , answer , time) from '%s%s%s%s' delimiter ';' CSV HEADER escape '\\' quote '"' """ % (
#                             year, month, day, dir, fn, account, table_name), sys.stdout)
#                         page += 'THANKS TINH YEU (♥_♥)  \n     '  # file was uploaded %s%s%s'%(fn,account,table_name)
#                     # page += 'The file "' + fn + '" was uploaded and import successfully'
#
#                     # page += "Upload file sucessfull"
#                     # #xoa file vua gui len
#                     # try:
#                     #	os.remove('/usr/local/www/apache24/wsgi-scripts/file_upload/' + fn + account + '%s_%s_%s_%s_%s_%s.csv'%(year,month,day,hour,minute,second))
#                     # except OSError:
#                     #	pass
#                     except IOError as err:
#                         page += "I/O error: {0}".format(err)
#                     except ValueError:
#                         page += "Could not import data file csv to database"
#                         raise

                        # cur.execute("update omnivore_%s_%s_%s set answer= replace(answer,'unselected','') where answer ilike '%%unselected%%'"%(year,month,day))
                        # conn.commit()
                        # cur.execute("update omnivore_%s_%s_%s set answer= 'c' where answer ='unselectedc'"%(year,month,day))
                        # conn.commit()
        page += "hello"
    else:
        # page = "ok"
        page = u"""
            <html>
            <head><title>Upload</title></head>
            <body>
            <form name="test" method="post" action="" enctype="multipart/form-data">
                Import file csv : <input type="file" name="file" multiple/> <br />
                <p>--------------</p>
    
                <!--Upload file anh va excel:<br />
                <input type="file" name="file2" multiple/><br />
                <input type="file" name="file3" multiple/><br />-->
                <input type="submit" name="submit" value="Submit" />
            </form>
            <p>Note: files with the same name with overwrite any existing files.</p>
            </body>
            </html>
            """

    conn.commit()
    cur.close()
    conn.close()

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)

