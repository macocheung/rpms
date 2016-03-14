-- ----------------------------------------------------------------------------
-- ASTERISK-RPM - RPMs for Asterisk
-- Copyright (C) 2016 Paul Dugas.  All rights reserved.
-- ----------------------------------------------------------------------------
-- Package   RPMS
-- File      asterisk/asterisk.sql
-- Brief     SQL script for Asterisk
-- Author    Paul Dugas <paul@dugas.cc>
-- URL       https://github.com/pdugas/rpms/tree/master/asterisk
-- ----------------------------------------------------------------------------

-- ----------------------------------------------------------------------------
-- This script should be run as the "asterisk" user agains the "asterisk" 
-- database which should be setup like so.
--
--   # mysql 
--   ...
--   MariaDB [(none)]> create database asterisk; 
--   MariaDB [(none)]> grant all on asterisk.* to 'asterisk' identified by 'secret';
--
-- Replace "secret" with something better.!  Then load this script like
--   
--   # mysql -u asterisk -p asterisk < /usr/share/doc/asterisk-*/asterisk.sql
--
-- ----------------------------------------------------------------------------

-- Call Detail Records
DROP TABLE IF EXISTS `cdr`; 
CREATE TABLE `cdr` ( 
      'accountcode' varchar(20), 
      'src' varchar(80), 
      'dst' varchar(80), 
      'dcontext' varchar(80), 
      'clid' varchar(80), 
      'channel' varchar(80), 
      'dstchannel' varchar(80), 
      'lastapp' varchar(80), 
      'lastdata' varchar(80), 
      'start' datetime, 
      'answer' datetime, 
      'end' datetime, 
      'duration' integer, 
      'billsec' integer, 
      'disposition' varchar(45), 
      'amaflags' varchar(45), 
      'userfield' varchar(1024), 
      'uniqueid' varchar(150), 
      'linkedid' varchar(150), 
      'peeraccount' varchar(20), 
      'sequence' integer 
); 
ALTER TABLE `cdr` ADD INDEX by_start_answer_end (start,answer,end); 
ALTER TABLE `cdr` ADD INDEX by_src_dest (src,dst); 
ALTER TABLE `cdr` ADD INDEX by_accountcode (accountcode); 

-- CallerID 
DROP TABLE IF EXISTS `cid`; 
CREATE TABLE `cid` ( 
    `num` varchar(80) NOT NULL, 
    `name` varchar(255) NOT NULL default '', 
    `blacklist` tinyint(4) NOT NULL default '0', 
    `last_call` datetime NOT NULL default '0000-00-00 00:00:00', 
    `num_calls` int(11) NOT NULL default '0', 
    `groups` varchar(255) NOT NULL default '', 
    `notes` text NOT NULL, 
    PRIMARY KEY  (`num`) 
); 

-- ----------------------------------------------------------------------------
-- EOF
