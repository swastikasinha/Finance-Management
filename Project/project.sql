create schema if not exists project;

use project;

create table if not exists user(
UserID int not null auto_increment primary key, 
UserName varchar(100), 
email varchar(100), 
Password varchar(100), 
Age int, 
Income decimal(10,2), 
mobile_no char(10));

create table if not exists budget(
BudgetID int not null auto_increment primary key,
UserID int not null,
Year int,
Month int,
Budget int,
name varchar(100),
FOREIGN KEY (UserID) REFERENCES user(UserID)
);