# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
from gluon.debug import dbg
from datetime import datetime
import re
import HTMLParser
import logging

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

def listing():
    response.title = "web2py's sample 4 " + str(datetime.today())
    
#    logger.info('write the pdf heading')
    # define header and footers:
    head = THEAD(TR(TH("Header my1",_width="15%"), 
                    TH("Header 2",_width="65%"),
                    TH("Header 3",_width="20%"), 
                    _bgcolor="#A0A0A0"))
    foot = TFOOT(TR(TH("Footer 1",_width="15%"), 
                    TH("Footer 2",_width="65%"),
                    TH("Footer 3",_width="20%"),
                    _bgcolor="#E0E0E0"))
    
    # create several rows:
    row_data = db(db.sample.id>0).select()
    rows = []
    for r in row_data:
        
        rows.append(TR(TD(r.name, _width='15%'),
                       TD(r.story, _width='65%', _align="center"),
                       TD(r.result, _align="right", _width='20%'))) 

    # make the table object
    body = TBODY(*rows)
    table = TABLE(*[head,foot, body], 
                  _border="1", _align="center", _width="100%")

    if request.extension=="pdf":
       
        #from gluon.contrib.fpdf import FPDF
        from applications.report.modules import FPDF, HTMLMixin
        # define our FPDF class (move to modules if it is reused  frequently)
        class MyFPDF(FPDF, HTMLMixin):
            def header(self):
                self.set_font('Arial','B',15)
                self.cell(0,10, response.title ,1,0,'C')
                self.ln(20)
                
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial','I',8)
                txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
                self.cell(0,10,txt,0,0,'C')
                    
        pdf=MyFPDF()
        # first page:
        pdf.add_page()
      #  dbg.set_trace()
       
#        logger.info('Start of test')
        
        f=open("testdata.txt","w")
        f.write(html_unescape(str(table)))
        
        pdf.write_html(str(XML(table)))
        tab = "<table border='1' frame='border'><tr><td width='20%'>hello <></td><td width='20%'>world</td></tr></table>"
        for i in range(20):
            pdf.cell(20,5,"hello <&>",1 )
            pdf.multi_cell(20,5,"world's \n leading \n coder",1, 1)
        pdf.write_html("<p> added & <>paragraph </p>")
        response.headers['Content-Type']='application/pdf'
        return pdf.output(dest='S')
    else:
        # normal html view:
        return dict(table=table)
    
    
    
def report():
    data = "abc, def, ghi, jkl"
    return data

from htmlentitydefs import name2codepoint 
def replace_entities(match): 
    try: 
        ent = match.group(1) 
        if ent[0] == "#": 
            if ent[1] == 'x' or ent[1] == 'X': 
                return unichr(int(ent[2:], 16)) 
            else: 
                return unichr(int(ent[1:], 10)) 
        return unichr(name2codepoint[ent]) 
    except: 
        return match.group() 

entity_re = re.compile(r'&(#?[A-Za-z0-9]+?);') 

def html_unescape(data): 
    return entity_re.sub(replace_entities, data) 

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
