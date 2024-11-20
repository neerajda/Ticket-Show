# ticket_show
## Description
Ticket show is a multi user (user & admin) app where users can book tickets on a venue for
a show.He can book bulk tickets.And where admin can add multiple venues with multiple
shows.
Frameworks used
Flask:main framework
Render_template,redirect,url_for: to display the html content
Request:to get data from form
Flask_sqlalchemy:to map user input data to the database
DB Schema Design
1. User table with columns like user_id,username,password.
2. Admin table with columns like admin_id,admin_name,admin_password.
3. Venue table with columns like
venue_id,venue_name,venue_location,venue_capacity.
4. Show table with columns like
show_id,show_name,show_rating,show_tags,ticketprice,start_time,end_time.
5. Book_tickets table with columns like user_id,venue_id,show_id,time,number_tickts.
6. Show_admin table with columns like show_id and admin_id.
7. Venue_admin table with columns like venue_id and admin_id.
8. Venue_show table with columns like venue_id and show_id.

## Architecture and Features
Login system: A login system with password and username or adminname.
Styling:Complete CSS
## Functions:
1. Home:
1.1. Default route “/”: first page of the website which takes you to the home page
where you can see the available venue.
2. User:
2.1. “/shows/<int:venue_id>”:This route gives all shows related to a given venue.
2.2. “/userregister”:Through this route new user can register on the website.
2.3. “/user/login”:User login.
3. Admin:
3.1. “/adminregister”:New admin can make a account through this route.
3.2. “/admin/login”:Admin login.
3.3. “/adminpage/<int:admin_id>”:
3.4. “/adminshows/<int:venue_id>/<int:admin_id>”: this route shows all shows that
belong to a particular admin and a particular venue.
4. Venue Management:
4.1. “/addvenue/<int:admin_id>”: An admin can add a new venue.
4.2. “/edit/<int:venue_id>/<int:admin_id>”:An admin can edit the given venue
information.
4.3. “/remove/<int:venue_id>/<int:admin_id>”: Admin can delete the venue.
5. Show Management
5.1. “/addshow/<int:venue_id>/<int:admin_id>”:An admin can add a new show.
5.2. “/showedit/<int:show_id>/<int:venue_id>”: An admin can edit the show
information.
5.3. “/showremove/<int:show_id>/<int:venue_id>/<int:admin_id>”: Admin can
delete the show.
6. Ticket booking:
6.1. “/booking/<int:venue_id>/<int:show_id>”: It gives the form to the user using
booking details.
6.2. “/booked/<int:venue_id>/<int:show_id>”: This shows the booking
confirmation.
Video link
https://drive.google.com/file/d/1cuAkd7Ikd4czl4LCKLIDA46cfeI1bZ6Y/view?usp=sharing
