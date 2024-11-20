import os
from flask import Flask
from flask import render_template, request, redirect, url_for
from flask import request






from flask_sqlalchemy import SQLAlchemy
current_dir=os.path.abspath(os.path.dirname(__file__))


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"ticket.sqlit3.db")
db = SQLAlchemy()
db.init_app(app)




class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True,nullable=False)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.Integer, nullable=False)
    bookedtickets=db.relationship("Bookticket",backref="user")
   
    


class Admin(db.Model):
    __tablename__='admin'
    admin_id=db.Column(db.Integer,primary_key=True,nullable=False)
    admin_name=db.Column(db.String,nullable=False)
    admin_password=db.Column(db.Integer, nullable=False)
    venues=db.relationship("Venue",backref="admin",secondary="venue_admin")
    shows=db.relationship("Show",backref="admin",secondary="show_admin")
   



class Venue(db.Model):
    __talbename__='venue'
    venue_id=db.Column(db.Integer,nullable=False,primary_key=True)
    venue_name=db.Column(db.String,nullable=False)
    venue_capacity=db.Column(db.Integer, nullable=False)
    venue_location=db.Column(db.String, nullable=False)
    shows=db.relationship("Show", backref="venue",secondary="venue_show")  
class Show(db.Model):
    __tablename__='show'
    show_id=db.Column(db.Integer,nullable=False,primary_key=True)
    show_name=db.Column(db.String,nullable=False)
    show_rating=db.Column(db.Integer)
    show_tags=db.Column(db.String)
    ticketprice=db.Column(db.Integer, nullable=False)
    start_time=db.Column()
    end_time=db.Column()

class VenueShow(db.Model):
    __tablename__='venue_show'
    venue_id=db.Column(db.Integer,db.ForeignKey("venue.venue_id"),primary_key=True,nullable=False)
    show_id=db.Column(db.Integer, db.ForeignKey("show.show_id"),primary_key=True,nullable=False)
    


class VenueAdmin(db.Model):
    __tablename__='venue_admin'
    venue_id=db.Column(db.Integer,db.ForeignKey("venue.venue_id"),primary_key=True,nullable=False)
    admin_id=db.Column(db.Integer, db.ForeignKey("admin.admin_id"),primary_key=True,nullable=False)


class ShowAdmin(db.Model):
    __tablename__='show_admin'
    show_id=db.Column(db.Integer,db.ForeignKey("show.show_id"),primary_key=True,nullable=False)
    admin_id=db.Column(db.Integer, db.ForeignKey("admin.admin_id"),primary_key=True,nullable=False)

class Bookticket(db.Model):
    __tablename__="book_tickets"
    show_id=db.Column(db.Integer,db.ForeignKey("show.show_id"),primary_key=True,nullable=False)
    venue_id=db.Column(db.Integer,db.ForeignKey("venue.venue_id"),primary_key=True,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),primary_key=True,nullable=False)
    time=db.Column(db.Integer)
    number_tickts=db.Column(db.Integer)








































#Controllers

#Home Page
@app.route('/',methods=["GET","POST"])
def home():
    venues=Venue.query.all()
    return render_template("home.html",venues=venues)


#Show Page
@app.route("/shows/<int:venue_id>",methods=["GET","POST"])
def shows(venue_id):
    venue=Venue.query.get(venue_id)
    allshows=venue.shows
    return render_template("show.html",shows=allshows,venue=venue)


#User registeration page
@app.route('/userregister',methods=["GET","POST"])
def userregister():
    if request.method=="POST":
        username=request.form['u_name']
        user_password=request.form['password']
        us=User(username=username,
        password=user_password)
        db.session.add(us)
        db.session.commit()
        q=db.session.query(User).filter_by(username=username,password=user_password).first()
        venues=Venue.query.all()
        return render_template("userpage.html",q=q,venues=venues)
    return render_template("userregister.html")


#Userlogin Page
@app.route('/user/login',methods=["GET","POST"])
def user():
    if request.method=="POST":
        user_name=request.form['u_name']
        user_password=request.form['password']
        q=db.session.query(User).filter_by(username=user_name,password=user_password).first()
        venues=Venue.query.all()
        if q!=None:
            return render_template("userpage.html", q=q,venues=venues)
        
     
    return render_template("userlogin.html")

#Admin registeration page
@app.route("/adminregister",methods=["POST","GET"])
def adminregister():
    if request.method=="POST":
        admin_name=request.form['admin_name']
        admin_password=request.form['admin_password']
        us=Admin(admin_name=admin_name,
            admin_password=admin_password)
        db.session.add(us)
        db.session.commit()
        admin=db.session.query(Admin).filter_by(admin_name=admin_name,admin_password=admin_password).first()
        return redirect(url_for('adminpage',admin_id=admin.admin_id))
    return render_template("adminregister.html")




#Adminlogin login Page
@app.route('/admin/login',methods=["GET","POST"])
def adminlogin():
    if request.method=="POST":
        admin_name=request.form['a_name']
        admin_password=request.form['a_password']
        admin=db.session.query(Admin).filter_by(admin_name=admin_name,admin_password=admin_password).first()
        if admin!=None:
            allvenues=admin.venues
            allshows=admin.shows
            return render_template("newadminpage.html",venues=allvenues,shows=allshows,admin=admin)
          
        else:
            redirect("/adminregister")
       
    return render_template("adminlogin.html")



#Admin page
@app.route("/adminpage/<int:admin_id>",methods=["POST","GET"])
def adminpage(admin_id):
    if request.method=="GET":
        admin=Admin.query.get(admin_id)
        if admin!=None:
            allvenues=admin.venues
            allshows=admin.shows
            return render_template("newadminpage.html",venues=allvenues,shows=allshows,admin=admin)
            
        else:
            return render_template("adminregister.html")


#Venue Management
##Addvenue
@app.route("/addvenue/<int:admin_id>",methods=["GET","POST"])
def addvenue(admin_id):
    if request.method=="POST":
        admin=Admin.query.get(admin_id)
        venue_name=request.form['venue_name']
        venue_location=request.form['venue_location']
        venue_capacity=request.form['venue_capacity']
        venue=Venue(venue_name=venue_name,venue_location=venue_location,venue_capacity=venue_capacity)
        db.session.add(venue)
        db.session.commit()
        admin.venues.append(venue)
        db.session.commit()
        return redirect(url_for('adminpage',admin_id=admin_id)) 
    return render_template("addvenue.html",admin_id=admin_id) 

##Edit a venue
@app.route("/edit/<int:venue_id>/<int:admin_id>",methods=["GET","POST"])
def venueedit(venue_id,admin_id):
    venue=Venue.query.get(venue_id)
    if request.method=="GET":
        return render_template("editpage.html",venue=venue,admin_id=admin_id)
    if request.method=="POST":
        new_venue_name=request.form['new_venue_name']
        new_venue_location=request.form['new_venue_location']
        new_venue_capacity=request.form['new_venue_capacity']
        venue.venue_name=new_venue_name
        venue.venue_location=new_venue_location
        venue.venue_capacity=new_venue_capacity
        db.session.commit()
        return redirect(url_for('adminpage',admin_id=admin_id))

##Remove a venue
    
@app.route("/remove/<int:venue_id>/<int:admin_id>",methods=["GET","POST"])
def removevenue(venue_id,admin_id):
    venue=Venue.query.get(venue_id)
    if request.method=="GET":
        db.session.delete(venue)
        db.session.commit()
        return redirect(url_for('adminpage',admin_id=admin_id))

#Show Management
#Add a new Show
@app.route("/addshow/<int:venue_id>/<int:admin_id>",methods=["GET","POST"])
def addshow(admin_id,venue_id):
    if request.method=="POST":
        venue=Venue.query.get(venue_id)
        show_name=request.form['show_name']
        show_rating=request.form['show_rating']
        ticketprice=request.form['show_price']
        show_tags=request.form['show_tags']
        start_time=request.form['start_time']
        end_time=request.form['end_time']
        show=Show(show_name=show_name,show_rating=show_rating,ticketprice=ticketprice,show_tags=show_tags,start_time=start_time,end_time=end_time)
        db.session.add(show)                
        db.session.commit()
        venue.shows.append(show)
        db.session.commit()
        return redirect(url_for('adminshows',venue_id=venue_id,admin_id=admin_id))
    if request.method=="GET":
        venue=Venue.query.get(venue_id)
        return render_template("addshow.html",admin_id=admin_id,venue=venue)





  #Edit a show  

#Show edit
@app.route("/showedit/<int:show_id>/<int:admin_id>/<int:venue_id>",methods=["GET","POST"])
def showedit(show_id,admin_id,venue_id):
    
    if request.method=="GET":
        return render_template("editshow.html",show_id=show_id,admin_id=admin_id,venue_id=venue_id)
    elif request.method=="POST":
        show=Show.query.get(show_id)
        new_show_name=request.form['new_show_name']
        new_show_tag=request.form['new_show_tag']
        new_show_ticketprice=request.form['new_show_ticketprice']
        show.show_name=new_show_name
        show.show_tag=new_show_tag
        show.ticketprice=new_show_ticketprice
        db.session.commit()
        return redirect(url_for('adminshows',venue_id=venue_id,admin_id=admin_id))


##Remove a show
    
@app.route("/showremove/<int:show_id>/<int:venue_id>/<int:admin_id>",methods=["GET","POST"])
def remoshow(show_id,venue_id,admin_id):
    show=Show.query.get(show_id)
    if request.method=="GET":
        db.session.delete(show)
        db.session.commit()
        return redirect(url_for('adminshows',admin_id=admin_id,venue_id=venue_id))



#Admin show page
#Show Page
@app.route("/adminshows/<int:venue_id>/<int:admin_id>",methods=["GET","POST"])
def adminshows(venue_id,admin_id):
    if request.method=="GET":
        venue=Venue.query.get(venue_id)
        allshows=venue.shows
        return render_template("adminshowpage.html",shows=allshows,venue=venue,admin_id=admin_id) 


#Booking page
@app.route("/booking/<int:venue_id>/<int:show_id>",methods=["GET","POST"])
def booking(venue_id,show_id):
    venue=Venue.query.get(venue_id)
    show=Show.query.get(show_id)
    #q=db.session.query(User).filter_by(user_id=user_id).first()
    return render_template("bookingpage.html",venue=venue,show=show,)


 
 #Booked
@app.route("/booked/<int:venue_id>/<int:show_id>",methods=["GET","POST"])
def booked(venue_id,show_id):
    venue=Venue.query.filter_by(venue_id=venue_id).first()
    show=Show.query.filter_by(show_id=show_id).first()
    user_name=request.form['u_name']
    user_password=request.form['password']
    number_tickts=request.form['number_tickts']
    q=db.session.query(User).filter_by(username=user_name,password=user_password).first()
    if q!=None:
        user_id=q.user_id
        show_id=show.show_id
        venue_id=venue_id
        book=Bookticket(user_id=user_id,show_id=show_id,venue_id=venue_id,number_tickts=number_tickts)
        db.session.add(book)
        db.session.commit()
        return render_template("booked.html", q=q,venue=venue,show=show)










        


 












































#Search function
@app.route('/search',methods=["POST"])
def search():
    if request.method=="POST":
        search=request.form["search"]
        venues=Venue.query.filter_by(venue_location=Venue.venue_location.like('%'+search+'%'))
        
        render_template("search.html",search=search,venue=venues)
    


if __name__=='__main__':
    #Run flask app
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080)