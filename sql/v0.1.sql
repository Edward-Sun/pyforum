-- ----------------------------
--  Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `role_id` SMALLINT(4)  DEFAULT 0 NOT NULL COMMENT '角色id',
  `confirmed` tinyint(1) unsigned DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 后台路由模块表
CREATE TABLE `manage_module` (
  `id`        INT(10) UNSIGNED        NOT NULL AUTO_INCREMENT,
  `parent_id` INT(10) UNSIGNED        NOT NULL DEFAULT '0'
  COMMENT '上级模块id',
  `name`      VARCHAR(20)
              COLLATE utf8_unicode_ci NOT NULL DEFAULT ''
  COMMENT '模块名称',
  `uri`       VARCHAR(50)
              COLLATE utf8_unicode_ci NOT NULL DEFAULT ''
  COMMENT '路径',
  `prefix`    VARCHAR(50)
              COLLATE utf8_unicode_ci NOT NULL DEFAULT ''
  COMMENT 'uri前缀',
  `weight`    SMALLINT(5) UNSIGNED    NOT NULL DEFAULT '0'
  COMMENT '权重越大越靠前',
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = '后台功能模块表';


ALTER TABLE `manage_module` ADD INDEX `i_parentid_weight`(`parent_id`,`weight`);

insert into manage_module(id,parent_id,name,uri,weight)values(1,0,'文章','/posts',900);
insert into manage_module(id,parent_id,name,uri,prefix,weight)values(2,1,'文章管理','/posts','/posts',900);
#用户角色说明------ 开始
DROP  TABLE IF EXISTS `user_role`;

CREATE TABLE `user_role` (
  `id`  SMALLINT(4)  UNSIGNED NOT NULL COMMENT '角色id',
  `des` VARCHAR(100) NOT NULL  DEFAULT ''
  COMMENT '角色说明',
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = '用户角色说明表';
INSERT INTO `user_role` (id, des) VALUES (1, '普通用户');
INSERT INTO `user_role` (id, des) VALUES (4, '小编');
INSERT INTO `user_role` (id, des) VALUES (256, '管理员');
#用户角色说明------ 结束

#角色模块表 -----开始

DROP TABLE IF EXISTS `role_module`;
CREATE TABLE `role_module` (
  `id`        INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_id`   SMALLINT(4) UNSIGNED      NOT NULL DEFAULT 20
  COMMENT '用户角色id, 0:普通用户, 256:管理员',
  `module_id` INT(10) UNSIGNED NOT NULL
  COMMENT '模块id',
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COMMENT = '角色-模块表';

ALTER TABLE `role_module` ADD  INDEX `i_role_id`(`role_id`);
INSERT INTO `role_module` (`role_id`,`module_id`) VALUES (256,1),(256,2);

#角色模块表 -----结束


#文章表-------开始
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL COMMENT '帖子标题',
  `user_id` int unsigned NOT NULL COMMENT '作者id',
  `summary` text NOT NULL COMMENT '快照(缩略总结)',
  `content` text NOT NULL COMMENT '内容',
  `created_at` int unsigned NOT NULL COMMENT '帖子创建时间',
  `updated_at` int unsigned NOT NULL COMMENT '帖子修改时间',
  `posted_at` int unsigned NOT NULL COMMENT '帖子发布时间',
  `read_count` int unsigned NOT NULL DEFAULT 0 COMMENT '阅读数',
  `like_count` int unsigned NOT NULL DEFAULT 0 COMMENT '点赞数',
  `comment_floor` int unsigned NOT NULL DEFAULT 0 COMMENT '评论当前楼层',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='文章';
#文章表------结束

#测试数据
INSERT INTO `post` (`title`,`user_id`,`summary`,`content`,`created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试1',25,'测试1sumamry','测试1内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`summary`,`content`,`created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试2',25,'测试1sumamry','测试1内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`summary`,`content`,`created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试3',25,'测试1sumamry','测试1内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`summary`,`content`,`created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试4',25,'测试1sumamry','测试1内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`summary`,`content`,`created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试5',25,'测试1sumamry','测试1内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`summary`,`content`,`created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试6',25,'测试1sumamry','测试1内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);
INSERT INTO `post` (`title`,`user_id`,`summary`,`content`,`created_at`,`posted_at`,`updated_at`,`read_count`,`like_count`,`comment_floor`)
    VALUES ('测试7',25,'测试1sumamry','测试1内容',UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),UNIX_TIMESTAMP(),0,0,0);


CREATE TABLE `post_tag` (
  `tag_name` varchar(60) NOT NULL COMMENT '文章标签名字', -- 标签名字，唯一
  `visit_count` int unsigned NOT NULL DEFAULT 0, -- 标签的访问次数
  PRIMARY KEY (`tag_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '帖子标签';

CREATE TABLE `post_tag_relate` (
   `id` int unsigned NOT NULL AUTO_INCREMENT,
    `post_id` int unsigned NOT NULL ,
   `tag_name` varchar(60) NOT NULL COMMENT '标签名字',-- 标签名字
  PRIMARY KEY (`id`),
  INDEX(`post_id`),
  INDEX (`tag_name`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '帖子标签对应';



