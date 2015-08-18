-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 18, 2015 at 06:28 PM
-- Server version: 5.5.43-0ubuntu0.14.04.1
-- PHP Version: 5.6.11-1+deb.sury.org~trusty+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `soapbox`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=64 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add group', 3, 'add_group'),
(8, 'Can change group', 3, 'change_group'),
(9, 'Can delete group', 3, 'delete_group'),
(10, 'Can add user', 4, 'add_user'),
(11, 'Can change user', 4, 'change_user'),
(12, 'Can delete user', 4, 'delete_user'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add users', 7, 'add_users'),
(20, 'Can change users', 7, 'change_users'),
(21, 'Can delete users', 7, 'delete_users'),
(22, 'Can add personal details', 8, 'add_personaldetails'),
(23, 'Can change personal details', 8, 'change_personaldetails'),
(24, 'Can delete personal details', 8, 'delete_personaldetails'),
(25, 'Can add chat mod', 9, 'add_chatmod'),
(26, 'Can change chat mod', 9, 'change_chatmod'),
(27, 'Can delete chat mod', 9, 'delete_chatmod'),
(28, 'Can add user status', 10, 'add_userstatus'),
(29, 'Can change user status', 10, 'change_userstatus'),
(30, 'Can delete user status', 10, 'delete_userstatus'),
(31, 'Can add user image', 11, 'add_userimage'),
(32, 'Can change user image', 11, 'change_userimage'),
(33, 'Can delete user image', 11, 'delete_userimage'),
(34, 'Can add user followers', 12, 'add_userfollowers'),
(35, 'Can change user followers', 12, 'change_userfollowers'),
(36, 'Can delete user followers', 12, 'delete_userfollowers'),
(37, 'Can add categories', 13, 'add_categories'),
(38, 'Can change categories', 13, 'change_categories'),
(39, 'Can delete categories', 13, 'delete_categories'),
(40, 'Can add group users category', 14, 'add_groupuserscategory'),
(41, 'Can change group users category', 14, 'change_groupuserscategory'),
(42, 'Can delete group users category', 14, 'delete_groupuserscategory'),
(43, 'Can add posts', 15, 'add_posts'),
(44, 'Can change posts', 15, 'change_posts'),
(45, 'Can delete posts', 15, 'delete_posts'),
(46, 'Can add post categories', 16, 'add_postcategories'),
(47, 'Can change post categories', 16, 'change_postcategories'),
(48, 'Can delete post categories', 16, 'delete_postcategories'),
(49, 'Can add post likes', 17, 'add_postlikes'),
(50, 'Can change post likes', 17, 'change_postlikes'),
(51, 'Can delete post likes', 17, 'delete_postlikes'),
(52, 'Can add post listens', 18, 'add_postlistens'),
(53, 'Can change post listens', 18, 'change_postlistens'),
(54, 'Can delete post listens', 18, 'delete_postlistens'),
(55, 'Can add post shares', 19, 'add_postshares'),
(56, 'Can change post shares', 19, 'change_postshares'),
(57, 'Can delete post shares', 19, 'delete_postshares'),
(58, 'Can add comments', 20, 'add_comments'),
(59, 'Can change comments', 20, 'change_comments'),
(60, 'Can delete comments', 20, 'delete_comments'),
(61, 'Can add podcast timer', 21, 'add_podcasttimer'),
(62, 'Can change podcast timer', 21, 'change_podcasttimer'),
(63, 'Can delete podcast timer', 21, 'delete_podcasttimer');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$20000$rzvSwKKiZku0$AG1/PVDy+7MR3HfqMIDwkaZrPzf0MX8iQ5VXMh34v1Q=', NULL, 1, 'root', '', '', 'deepak.u@iapptechnologies.com', 1, 1, '2015-08-18 12:25:37');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=22 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(13, 'soapbox', 'categories'),
(9, 'soapbox', 'chatmod'),
(20, 'soapbox', 'comments'),
(14, 'soapbox', 'groupuserscategory'),
(8, 'soapbox', 'personaldetails'),
(21, 'soapbox', 'podcasttimer'),
(16, 'soapbox', 'postcategories'),
(17, 'soapbox', 'postlikes'),
(18, 'soapbox', 'postlistens'),
(15, 'soapbox', 'posts'),
(19, 'soapbox', 'postshares'),
(12, 'soapbox', 'userfollowers'),
(11, 'soapbox', 'userimage'),
(7, 'soapbox', 'users'),
(10, 'soapbox', 'userstatus');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=17 ;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2015-08-18 12:23:58'),
(2, 'auth', '0001_initial', '2015-08-18 12:24:00'),
(3, 'admin', '0001_initial', '2015-08-18 12:24:01'),
(4, 'contenttypes', '0002_remove_content_type_name', '2015-08-18 12:24:01'),
(5, 'auth', '0002_alter_permission_name_max_length', '2015-08-18 12:24:02'),
(6, 'auth', '0003_alter_user_email_max_length', '2015-08-18 12:24:02'),
(7, 'auth', '0004_alter_user_username_opts', '2015-08-18 12:24:02'),
(8, 'auth', '0005_alter_user_last_login_null', '2015-08-18 12:24:02'),
(9, 'auth', '0006_require_contenttypes_0002', '2015-08-18 12:24:02'),
(10, 'sessions', '0001_initial', '2015-08-18 12:24:02'),
(11, 'soapbox', '0001_initial', '2015-08-18 12:24:14'),
(12, 'soapbox', '0002_auto_20150619_0549', '2015-08-18 12:24:15'),
(13, 'soapbox', '0003_auto_20150626_1137', '2015-08-18 12:24:23'),
(14, 'soapbox', '0004_auto_20150626_1139', '2015-08-18 12:24:35'),
(15, 'soapbox', '0005_auto_20150626_1143', '2015-08-18 12:24:46'),
(16, 'soapbox', '0006_auto_20150626_1147', '2015-08-18 12:25:00');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_categories`
--

CREATE TABLE IF NOT EXISTS `soapbox_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  `created_on` date NOT NULL,
  `created_at` time NOT NULL,
  `type_of_category` varchar(10) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_categories_e93cb7eb` (`created_by_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_chatmod`
--

CREATE TABLE IF NOT EXISTS `soapbox_chatmod` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jabber_id` bigint(20) NOT NULL,
  `jabber_password` varchar(72) NOT NULL,
  `juser_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_chatmod_bf3a2fb6` (`juser_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_comments`
--

CREATE TABLE IF NOT EXISTS `soapbox_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` longtext NOT NULL,
  `comment` longtext,
  `type_of_post` varchar(7) NOT NULL,
  `comment_on` date NOT NULL,
  `comment_at` time NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_comments_e8701ad4` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_groupuserscategory`
--

CREATE TABLE IF NOT EXISTS `soapbox_groupuserscategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_gr_category_id_25bf57b430eeaa94_fk_soapbox_categories_id` (`category_id`),
  KEY `soapbox_groupuserscategory_e8701ad4` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_personaldetails`
--

CREATE TABLE IF NOT EXISTS `soapbox_personaldetails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(40) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `dob` date DEFAULT NULL,
  `age` smallint(6) NOT NULL,
  `state` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `profile_img` varchar(250) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_personaldetails_e8701ad4` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_podcasttimer`
--

CREATE TABLE IF NOT EXISTS `soapbox_podcasttimer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timer` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_postcategories`
--

CREATE TABLE IF NOT EXISTS `soapbox_postcategories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_po_category_id_3be185d4b873e675_fk_soapbox_categories_id` (`category_id`),
  KEY `soapbox_postcategories_f3aa1999` (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_postlikes`
--

CREATE TABLE IF NOT EXISTS `soapbox_postlikes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num_likes` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_postlikes_f3aa1999` (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_postlistens`
--

CREATE TABLE IF NOT EXISTS `soapbox_postlistens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num_listens` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_postlistens_f3aa1999` (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_posts`
--

CREATE TABLE IF NOT EXISTS `soapbox_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_file_url` varchar(150) NOT NULL,
  `post_title` varchar(150) NOT NULL,
  `post_description` longtext NOT NULL,
  `posted_on` date NOT NULL,
  `posted_at` time NOT NULL,
  `user_by_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_posts_ffeda3e0` (`user_by_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_postshares`
--

CREATE TABLE IF NOT EXISTS `soapbox_postshares` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num_shares` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_postshares_post_id_ed594adba6e6b45_fk_soapbox_posts_id` (`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_userfollowers`
--

CREATE TABLE IF NOT EXISTS `soapbox_userfollowers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `follower_id_id` int(11) NOT NULL,
  `user_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `soapbox_userfollowers_39b12cc3` (`follower_id_id`),
  KEY `soapbox_userfollowers_18624dd3` (`user_id_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_userimage`
--

CREATE TABLE IF NOT EXISTS `soapbox_userimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profilepic` varchar(150) NOT NULL,
  `user_id` int(11) NOT NULL,
  `userimage_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `userimage_id` (`userimage_id`),
  KEY `soapbox_userimage_e8701ad4` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_users`
--

CREATE TABLE IF NOT EXISTS `soapbox_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(50) NOT NULL,
  `status` smallint(6) NOT NULL,
  `user_type` varchar(10) NOT NULL,
  `registered_thru` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `soapbox_userstatus`
--

CREATE TABLE IF NOT EXISTS `soapbox_userstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `about` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `usrst_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usrst_id` (`usrst_id`),
  KEY `soapbox_userstatus_user_id_9e2b94e7c7789c5_fk_soapbox_users_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `soapbox_categories`
--
ALTER TABLE `soapbox_categories`
  ADD CONSTRAINT `soapbox_categ_created_by_id_7b3e5cba7bdbe425_fk_soapbox_users_id` FOREIGN KEY (`created_by_id`) REFERENCES `soapbox_users` (`id`);

--
-- Constraints for table `soapbox_chatmod`
--
ALTER TABLE `soapbox_chatmod`
  ADD CONSTRAINT `soapbox_chatmod_juser_id_26b98066e5bd0e84_fk_soapbox_users_id` FOREIGN KEY (`juser_id`) REFERENCES `soapbox_users` (`id`);

--
-- Constraints for table `soapbox_comments`
--
ALTER TABLE `soapbox_comments`
  ADD CONSTRAINT `soapbox_comments_user_id_300be05b27295f6a_fk_soapbox_users_id` FOREIGN KEY (`user_id`) REFERENCES `soapbox_users` (`id`);

--
-- Constraints for table `soapbox_groupuserscategory`
--
ALTER TABLE `soapbox_groupuserscategory`
  ADD CONSTRAINT `soapbox_groupusersc_user_id_5e464d6ddd82e88d_fk_soapbox_users_id` FOREIGN KEY (`user_id`) REFERENCES `soapbox_users` (`id`),
  ADD CONSTRAINT `soapbox_gr_category_id_25bf57b430eeaa94_fk_soapbox_categories_id` FOREIGN KEY (`category_id`) REFERENCES `soapbox_categories` (`id`);

--
-- Constraints for table `soapbox_personaldetails`
--
ALTER TABLE `soapbox_personaldetails`
  ADD CONSTRAINT `soapbox_personaldeta_user_id_6c8fdad68042f85_fk_soapbox_users_id` FOREIGN KEY (`user_id`) REFERENCES `soapbox_users` (`id`);

--
-- Constraints for table `soapbox_postcategories`
--
ALTER TABLE `soapbox_postcategories`
  ADD CONSTRAINT `soapbox_postcategor_post_id_605944c4565e893d_fk_soapbox_posts_id` FOREIGN KEY (`post_id`) REFERENCES `soapbox_posts` (`id`),
  ADD CONSTRAINT `soapbox_po_category_id_3be185d4b873e675_fk_soapbox_categories_id` FOREIGN KEY (`category_id`) REFERENCES `soapbox_categories` (`id`);

--
-- Constraints for table `soapbox_postlikes`
--
ALTER TABLE `soapbox_postlikes`
  ADD CONSTRAINT `soapbox_postlikes_post_id_7a231d36508946da_fk_soapbox_posts_id` FOREIGN KEY (`post_id`) REFERENCES `soapbox_posts` (`id`);

--
-- Constraints for table `soapbox_postlistens`
--
ALTER TABLE `soapbox_postlistens`
  ADD CONSTRAINT `soapbox_postlistens_post_id_225a1a3ccbc50e7c_fk_soapbox_posts_id` FOREIGN KEY (`post_id`) REFERENCES `soapbox_posts` (`id`);

--
-- Constraints for table `soapbox_posts`
--
ALTER TABLE `soapbox_posts`
  ADD CONSTRAINT `soapbox_posts_user_by_id_139f2694250ce455_fk_soapbox_users_id` FOREIGN KEY (`user_by_id`) REFERENCES `soapbox_users` (`id`);

--
-- Constraints for table `soapbox_postshares`
--
ALTER TABLE `soapbox_postshares`
  ADD CONSTRAINT `soapbox_postshares_post_id_ed594adba6e6b45_fk_soapbox_posts_id` FOREIGN KEY (`post_id`) REFERENCES `soapbox_posts` (`id`);

--
-- Constraints for table `soapbox_userfollowers`
--
ALTER TABLE `soapbox_userfollowers`
  ADD CONSTRAINT `soapbox_userfollo_user_id_id_91096d075e82a04_fk_soapbox_users_id` FOREIGN KEY (`user_id_id`) REFERENCES `soapbox_users` (`id`),
  ADD CONSTRAINT `soapbox_user_follower_id_id_4c4b204a51ac3cef_fk_soapbox_users_id` FOREIGN KEY (`follower_id_id`) REFERENCES `soapbox_users` (`id`);

--
-- Constraints for table `soapbox_userimage`
--
ALTER TABLE `soapbox_userimage`
  ADD CONSTRAINT `soapbox_userim_userimage_id_519caf37ecc7c8c7_fk_soapbox_users_id` FOREIGN KEY (`userimage_id`) REFERENCES `soapbox_users` (`id`),
  ADD CONSTRAINT `soapbox_userimage_user_id_6f74a4b8854a4861_fk_soapbox_users_id` FOREIGN KEY (`user_id`) REFERENCES `soapbox_users` (`id`);

--
-- Constraints for table `soapbox_userstatus`
--
ALTER TABLE `soapbox_userstatus`
  ADD CONSTRAINT `soapbox_userstatus_usrst_id_619e398ff21c5b22_fk_soapbox_users_id` FOREIGN KEY (`usrst_id`) REFERENCES `soapbox_users` (`id`),
  ADD CONSTRAINT `soapbox_userstatus_user_id_9e2b94e7c7789c5_fk_soapbox_users_id` FOREIGN KEY (`user_id`) REFERENCES `soapbox_users` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
