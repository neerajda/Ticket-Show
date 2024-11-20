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
