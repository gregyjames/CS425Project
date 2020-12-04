CREATE TABLE "administrator"  ( 
	"admin_id"  	int AUTO_INCREMENT NOT NULL,
	"admin_name"	varchar(100) NOT NULL,
	PRIMARY KEY("admin_id") USING BTREE
)
GO
CREATE TABLE "building"  ( 
	"building_name"	varchar(80) NOT NULL,
	"fee"          	int NOT NULL,
	PRIMARY KEY("building_name") USING BTREE
)
GO
CREATE TABLE "calendar"  ( 
	"reservation_date"	date NOT NULL,
	"reservation_time"	time NOT NULL,
	PRIMARY KEY("reservation_date","reservation_time") USING BTREE
)
GO
CREATE TABLE "login"  ( 
	"id"           	int AUTO_INCREMENT NOT NULL,
	"login_time"   	datetime NOT NULL,
	"logout_time"  	datetime NOT NULL,
	"member_id"    	int NULL,
	"non_member_id"	int NULL,
	PRIMARY KEY("id") USING BTREE
)
GO
CREATE TABLE "members"  ( 
	"car_plate_no" 	varchar(20) NOT NULL,
	"fee_paid"     	double(16,4) NOT NULL,
	"full_name"    	varchar(100) NOT NULL,
	"member_id"    	int AUTO_INCREMENT NOT NULL,
	"temp_plate_no"	varchar(45) NULL,
	PRIMARY KEY("member_id") USING BTREE
)
GO
CREATE TABLE "non_member"  ( 
	"full_name"    	varchar(100) NOT NULL,
	"non_member_id"	int AUTO_INCREMENT NOT NULL,
	PRIMARY KEY("non_member_id") USING BTREE
)
GO
CREATE TABLE "parking_spot"  ( 
	"building_name"	varchar(100) NOT NULL,
	"lot_no"       	int NOT NULL,
	"spot_no"      	int NOT NULL,
	PRIMARY KEY("lot_no","spot_no","building_name") USING BTREE
)
GO
CREATE TABLE "reservation"  ( 
	"building_name"   	varchar(45) NOT NULL,
	"lot_no"          	varchar(45) NOT NULL,
	"member_id"       	int NULL,
	"non_member_id"   	int NULL,
	"reservation_date"	date NOT NULL,
	"reservation_id"  	int AUTO_INCREMENT NOT NULL,
	"reservation_time"	time NOT NULL,
	"spot_no"         	varchar(45) NOT NULL,
	PRIMARY KEY("reservation_id") USING BTREE
)
GO
CREATE TABLE "staff"  ( 
	"staff_id"  	int AUTO_INCREMENT NOT NULL,
	"staff_name"	varchar(100) NOT NULL,
	PRIMARY KEY("staff_id") USING BTREE
)
GO

CREATE INDEX "building_name" USING BTREE 
	ON "parking_spot"("building_name")
GO
CREATE INDEX "building_name_idx" USING BTREE 
	ON "reservation"("building_name")
GO
CREATE INDEX "date_idx" USING BTREE 
	ON "reservation"("reservation_date")
GO
CREATE INDEX "lot_no_idx" USING BTREE 
	ON "reservation"("lot_no")
GO
CREATE INDEX "member_id_idx" USING BTREE 
	ON "reservation"("member_id")
GO
CREATE INDEX "non_member_id_idx" USING BTREE 
	ON "reservation"("non_member_id")
GO
CREATE INDEX "spot_no_idx" USING BTREE 
	ON "reservation"("spot_no")
GO
CREATE INDEX "time_idx" USING BTREE 
	ON "reservation"("reservation_time")
GO
ALTER TABLE "parking_spot"
	ADD CONSTRAINT "building_name"
	FOREIGN KEY("building_name")
	REFERENCES "building"("building_name")
	ON DELETE NO ACTION
	ON UPDATE NO ACTION
GO
ALTER TABLE "reservation"
	ADD CONSTRAINT "reservation_date"
	FOREIGN KEY("reservation_date")
	REFERENCES "calendar"("reservation_date")
	ON DELETE NO ACTION
	ON UPDATE NO ACTION
GO
ALTER TABLE "reservation"
	ADD CONSTRAINT "non_member_id"
	FOREIGN KEY("non_member_id")
	REFERENCES "non_member"("non_member_id")
	ON DELETE NO ACTION
	ON UPDATE NO ACTION
GO
ALTER TABLE "reservation"
	ADD CONSTRAINT "member_id"
	FOREIGN KEY("member_id")
	REFERENCES "members"("member_id")
	ON DELETE NO ACTION
	ON UPDATE NO ACTION
GO
