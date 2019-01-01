DROP DATABASE IF EXISTS `pyforum`;
CREATE DATABASE `pyforum`;
USE pyforum;

-- ----------------------------
--  Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `role_id` SMALLINT(4)  DEFAULT 0 NOT NULL COMMENT '角色id',
  `confirmed` tinyint(1) unsigned DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT = '用户表';

INSERT INTO `user` (`id`,`username`,`email`,`password_hash`,`confirmed`)
    VALUES (1, 'szq', '569342215@qq.com', 'pbkdf2:sha1:1000$sheKmza5$95de7e0052f2dd2b533570a8c6850fee9a0c9ea4', '1');
INSERT INTO `user` (`id`,`username`,`email`,`password_hash`,`confirmed`)
    VALUES (2, 'szq2', '569342216@qq.com', 'pbkdf2:sha1:1000$sheKmza5$95de7e0052f2dd2b533570a8c6850fee9a0c9ea4', '1');

-- ----------------------------
--  Table structure for `module`
-- ----------------------------
DROP TABLE IF EXISTS `module`;
CREATE TABLE `module` (
  `id`        INT(10) UNSIGNED        NOT NULL AUTO_INCREMENT,
  `parent_id` INT(10) UNSIGNED        NOT NULL DEFAULT '0'
  COMMENT '上级模块id',
  `name`      VARCHAR(20)
              COLLATE utf8_unicode_ci NOT NULL DEFAULT ''
  COMMENT '模块名称',
  `url`       VARCHAR(50)
              COLLATE utf8_unicode_ci NOT NULL DEFAULT ''
  COMMENT '路径',
  `prefix`    VARCHAR(50)
              COLLATE utf8_unicode_ci NOT NULL DEFAULT ''
  COMMENT 'url前缀',
  `weight`    SMALLINT(5) UNSIGNED    NOT NULL DEFAULT '0'
  COMMENT '权重越大越靠前',
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COMMENT = '模块表';

insert into module(id,parent_id,name,url,weight) values(1,0,'版块1','/module/1',900);
insert into module(id,parent_id,name,url,weight) values(2,0,'版块2','/module/2',800);
insert into module(id,parent_id,name,url,weight) values(3,0,'版块3','/module/3',700);

#角色用户模块表 -----开始
DROP TABLE IF EXISTS `role_user_module`;
CREATE TABLE `role_user_module` (
  `role_id`   SMALLINT(4) UNSIGNED NOT NULL DEFAULT 20
  COMMENT '用户角色id, 20:普通用户, 256:管理员',
  `user_id` INT(10) UNSIGNED NOT NULL
  COMMENT '用户id',
  `module_id` INT(10) UNSIGNED NOT NULL
  COMMENT '模块id',
  UNIQUE KEY `i_role_user_module` (`role_id`, `user_id`, `module_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8 COMMENT = '角色-用户-模块表';

INSERT INTO `role_user_module` (`role_id`,`user_id`,`module_id`) VALUES (256,1,0), (0,2,1), (256,2,2);
#角色用户模块表 -----结束


#文章表-------开始
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL COMMENT '帖子标题',
  `user_id` int unsigned NOT NULL COMMENT '作者id',
  `module_id` int unsigned NOT NULL COMMENT '模块id',
  `content` text NOT NULL COMMENT '内容',
  `created_at` int unsigned NOT NULL COMMENT '帖子创建时间',
  `updated_at` int unsigned NOT NULL COMMENT '帖子修改时间',
  `posted_at` int unsigned NOT NULL  COMMENT '帖子发布时间',
  `read_count` int unsigned NOT NULL DEFAULT 0 COMMENT '阅读数',
  `like_count` int unsigned NOT NULL DEFAULT 0 COMMENT '点赞数',
  `comment_floor` int unsigned NOT NULL DEFAULT 0 COMMENT '评论当前楼层',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='文章';
#文章表------结束

#测试数据
INSERT INTO `post` (`title`,`user_id`,`module_id`,`content`,
                    `created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试1',1,1,'测试1内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`module_id`,`content`,
                    `created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试2',1,1,'测试2内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`module_id`,`content`,
                    `created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试3',1,2,'测试3内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`module_id`,`content`,
                    `created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试4',1,2,'测试4内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`module_id`,`content`,
                    `created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试5',2,1,'测试5内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`module_id`,`content`,
                    `created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试6',2,1,'测试6内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`module_id`,`content`,
                    `created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试7',2,2,'测试7内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);