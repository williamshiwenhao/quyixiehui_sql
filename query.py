sql = (
    (
        "协会自有演出场数",
        "SELECT COUNT(*) FROM `show` WHERE `type` IN ('own_outside','own_pku');"
    ),
    (
        "协会自有演出中的节目数",
        "SELECT COUNT(*) FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` WHERE s.`type` IN ('own_outside','own_pku');"
    ),
    (
        '协会自有演出中的unique的协会成员的人数',
        '''SELECT COUNT(DISTINCT m.`mid`) FROM ( SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` WHERE s.`type` IN ('own_outside','own_pku') ) AS p JOIN `program_member` AS pm ON pm.`pid` = p.`pid` JOIN `member` AS m ON pm.`mid` = m.`mid` WHERE (m.join_type IN ('normal', 'midterm') OR m.join_type IS NULL)'''
    ),
    (
        '上演次数最多的节目',
        'SELECT     program_name, COUNT(*) AS ct FROM     program_own_with_stat GROUP BY program_name HAVING ct >= 4 ORDER BY ct DESC '
    ),
    (
        '更多演员选择的节目(排除1中同一对演员反复演出的情况；如果只换了捧哏演员，是不是也可以视作没换？',
        'SELECT     program_name, COUNT(DISTINCT mid) AS ct FROM     program_own_with_stat AS p         JOIN     all_program_member AS pm ON p.pid = pm.pid WHERE     pm.position = 1 GROUP BY program_name HAVING ct>=4 ORDER BY ct DESC '
    ),
    (
        '原创节目，按演出时长排序(重复演员也重复)',
        '''SELECT     ap.`date`,     ap.`show`,     ap.program,     ap.duration,     ap.mid1,     ap.actor1,     ap.mid2,     ap.actor2,     ap.mid3,     ap.actor3 FROM     (SELECT         p.program_name, COUNT(*) AS ct     FROM         program_own_with_stat AS p     JOIN program_tag AS t ON p.pid = t.pid     WHERE         t.tag = 'yuanchuang'     GROUP BY program_name) AS p         JOIN     all_program AS ap ON p.program_name = ap.program         JOIN     program_tag AS pt ON pt.pid = ap.pid         JOIN     `show` AS s ON s.sid = ap.sid WHERE     pt.tag = 'yuanchuang'         AND s.`type` IN ('own_outside' , 'own_pku') ORDER BY p.ct DESC , ap.`date` '''
    ),
    (
        '改编节目，按演出次数排序(重复演员也重复算)',
        '''SELECT     p.program_name, COUNT(*) AS ct FROM     program_own_with_stat AS p         JOIN     program_tag AS t ON p.pid = t.pid WHERE     t.tag = 'gaibian' GROUP BY program_name ORDER BY ct DESC '''
    ),
    (
        '上演次数最少的传统节目',
        '''SELECT p.program_name, COUNT(*) AS ct FROM program_own_with_stat AS p WHERE p.program_type NOT IN ('non_xiangsheng' , 'kuaiban') AND pid NOT IN (SELECT DISTINCT pid FROM program_tag WHERE tag IN ('xiandai' , 'gaibian', 'yuanchuang', 'xiaoyuan', 'taiwan')) GROUP BY p.program_name ORDER BY ct DESC '''
    ),
    (
        '''单段时间最长的节目与演员''',
        '''SELECT `show`, s.date, program, duration, actor1, actor2, actor3 FROM all_program AS p JOIN show_own AS s ON p.sid = s.sid ORDER BY duration DESC LIMIT 20 '''
    ),
    (
        '单段时间最短的节目与演员',
        '''SELECT `show`, s.date, program, duration, actor1, actor2, actor3 FROM all_program AS p JOIN show_own AS s ON p.sid = s.sid WHERE duration IS NOT NULL ORDER BY duration ASC LIMIT 20 '''
    ),
    (
        '节目次数最多的演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM ( SELECT pm.`mid`, COUNT(*) mp_ct FROM ( SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` WHERE s.`type` IN ('own_outside','own_pku') ) AS p JOIN `program_member` AS pm ON pm.`pid` = p.`pid` WHERE pm.position<=3 GROUP BY pm.`mid` having mp_ct >=10 ORDER BY mp_ct DESC ) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '主持次数最多的主持人（目前需要针对双人主持进行手动调整，可考专场包括京科逗你玩、十周年第一场、欢乐送，需要增加黄敏骢1次、韩潇1次）',
        '''SELECT m.`name`, h.* FROM (SELECT s.hostid, COUNT(*) AS ct, MIN(s.`date`) AS first_time, s.`name` FROM `show` AS s WHERE s.`type` IN ('own_outside' , 'own_pku') GROUP BY s.hostid) AS h JOIN `member` AS m ON m.mid = h.hostid ORDER BY h.ct DESC , h.first_time '''
    ),
    (
        '逗哏次数最多的演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND p.type IN ('multiple' , 'double')) AS p JOIN (SELECT * FROM `program_member` WHERE position = 1) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` HAVING mp_ct >= 5 ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '捧哏次数最多的演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND p.type IN ('multiple' , 'double')) AS p JOIN (SELECT * FROM `program_member` WHERE position = 2) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` HAVING mp_ct >= 5 ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '单口次数最多的演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND p.type IN ('single')) AS p JOIN `program_member` AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid`'''
    ),
    (
        '群口(主导)次数最多的演员 #统计了捧哏、逗哏、腻缝',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND p.type IN ('multiple')) AS p JOIN (SELECT * FROM `program_member` WHERE position <= 3) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` HAVING mp_ct >= 2 ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '快板次数最多的演员(注意，代码要求与其他统计不同，并且建议手动删除那些不打板的捧哏)',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` JOIN program_tag AS pt ON p.pid = pt.pid WHERE s.`type` IN ('own_outside' , 'own_pku') AND (p.type IN ('kuaiban') OR pt.tag = 'kuaiban')) AS p JOIN (SELECT * FROM `program_member`) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '返场次数最多的演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM ( SELECT pm.`mid`, COUNT(*) mp_ct FROM ( SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` WHERE s.`type` IN ('own_outside','own_pku') AND p.has_encore <> 0 ) AS p JOIN ( select * from `program_member` ) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` ORDER BY mp_ct DESC ) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '次均时间最长的演员',
        '''SELECT m.mid, m.`name`, mct.avg_time, mct.cnt FROM (SELECT pm.`mid`, AVG(p.`duration`) avg_time, COUNT(*) cnt FROM (SELECT p.`pid`, p.`name`, p.`duration` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` WHERE s.`type` IN ('own_outside' , 'own_pku')) AS p JOIN `program_member` AS pm ON pm.`pid` = p.`pid` WHERE pm.position <= 3 GROUP BY pm.`mid` ORDER BY avg_time DESC LIMIT 40) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '贯口次数最多的逗哏',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` JOIN `program_tag` AS pt ON p.`pid` = pt.`pid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND pt.tag = 'guankou') AS p JOIN (SELECT * FROM `program_member`) AS pm ON pm.`pid` = p.`pid` WHERE pm.position = 1 GROUP BY pm.`mid` HAVING mp_ct >= 2 ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '伦理次数最多的逗哏演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` JOIN `program_tag` AS pt ON p.`pid` = pt.`pid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND p.type IN ('double' , 'multiple') AND pt.tag = 'lunli') AS p JOIN (SELECT * FROM `program_member` WHERE position = 1) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '伦理次数最多的捧哏演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` JOIN `program_tag` AS pt ON p.`pid` = pt.`pid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND p.type IN ('double' , 'multiple') AND pt.tag = 'lunli') AS p JOIN (SELECT * FROM `program_member` WHERE position = 2) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` ORDER BY mp_ct DESC ) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '腿子+柳活最多的演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` JOIN `program_tag` AS pt ON p.`pid` = pt.`pid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND pt.tag IN ('tuizihuo' , 'liuhuo')) AS p JOIN (SELECT * FROM `program_member`) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '打哏最多的逗哏演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` JOIN `program_tag` AS pt ON p.`pid` = pt.`pid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND pt.tag IN ('dagen')) AS p JOIN (SELECT * FROM `program_member` WHERE position = 1) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '打哏最多的捧哏演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` JOIN `program_tag` AS pt ON p.`pid` = pt.`pid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND pt.tag IN ('dagen')) AS p JOIN (SELECT * FROM `program_member` WHERE position = 2) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` '''
    ),
    (
        '校园节目次数最多的演员',
        '''SELECT m.mid, m.`name`, mct.mp_ct FROM (SELECT pm.`mid`, COUNT(*) mp_ct FROM (SELECT p.`pid`, p.`name` FROM `show` AS s JOIN `program` AS p ON s.`sid` = p.`sid` JOIN `program_tag` AS pt ON p.`pid` = pt.`pid` WHERE s.`type` IN ('own_outside' , 'own_pku') AND pt.tag IN ('xiaoyuan')) AS p JOIN (SELECT * FROM `program_member` ) AS pm ON pm.`pid` = p.`pid` GROUP BY pm.`mid` ORDER BY mp_ct DESC) AS mct JOIN `member` AS m ON mct.`mid` = m.`mid` ''', \
        ),
    (
        '攒底次数最多的演员',
        '''SELECT  m.mid, m.`name`, COUNT(*) AS ct FROM  program_own_with_stat AS ps  JOIN  program_member AS pm ON pm.pid = ps.pid  JOIN  `member` AS m ON m.mid = pm.mid WHERE  ps.sequence = ps.max_sequence  AND pm.position <= 3 GROUP BY m.mid HAVING ct >= 2 ORDER BY ct DESC, m.mid '''
    ),
    (
        '攒底次数最多的搭档，捧逗顺序不限',
        '''SELECT mid1, m1.name AS name1, mid2, m2.name AS name2, ct FROM (SELECT pm1.mid AS mid1, pm2.mid AS mid2, COUNT(*) AS ct FROM program_own_with_stat AS p JOIN program_member AS pm1 ON pm1.pid = p.pid AND pm1.position < 3 JOIN program_member AS pm2 ON pm2.pid = p.pid AND pm1.mid < pm2.mid AND pm2.position < 3 WHERE p.sequence = p.max_sequence GROUP BY mid1 , mid2 HAVING ct >= 2) AS c JOIN `member` AS m1 ON c.mid1 = m1.mid JOIN `member` AS m2 ON c.mid2 = m2.mid ORDER BY ct DESC , mid1 , mid2 '''
    ),
    (
        '搭档人数最多的演员',
        '''SELECT m1.mid, m1.name, COUNT(DISTINCT m2.mid) AS ct FROM all_program_member AS m1 LEFT JOIN all_program_member AS m2 ON m1.pid = m2.pid AND m1.mid <> m2.mid WHERE m1.position < 4 AND (m2.position < 4 OR m2.mid IS NULL) GROUP BY m1.mid , m1.name ORDER BY ct DESC '''
    ),
    (
        '个人跨度最久的演员：第一段节目和最后一段节目之间，包含的学期数',
        '''SELECT pm.mid, pm.name, ROUND((MAX(xueqi) - MIN(xueqi)) * 2 + 1) AS xueqi_span, MIN(xueqi) xueqi_min, MAX(xueqi) xueqi_max FROM program_own_with_stat AS p JOIN all_program_member AS pm ON p.pid = pm.pid GROUP BY mid , name HAVING xueqi_span >= 10 ORDER BY xueqi_span DESC '''
    ),
    (
        '最固定的搭档：两个人共同(含大群口但是只算一二位)出现的节目次数，捧逗顺序不限',
        '''SELECT mid1, m1.`name` AS name1, mid2, m2.`name` AS name2, ct FROM (SELECT pm1.mid AS mid1, pm2.mid AS mid2, COUNT(*) AS ct FROM program_own_with_stat AS p JOIN program_member AS pm1 ON pm1.pid = p.pid AND pm1.`position` < 3 JOIN program_member AS pm2 ON pm2.pid = p.pid AND pm1.mid < pm2.mid AND pm2.`position` < 3 GROUP BY mid1 , mid2 HAVING ct > 2) AS c JOIN `member` AS m1 ON c.mid1 = m1.mid JOIN `member`AS m2 ON c.mid2 = m2.mid ORDER BY ct DESC , mid1 , mid2 '''
    ),
    (
        '节目次数最多的女演员',
        '''SELECT pm.mid, pm.name, COUNT(*) AS ct FROM program_own_with_stat AS p JOIN all_program_member pm ON p.pid = pm.pid WHERE pm.gender = 'female' AND pm.position < 4 GROUP BY mid , name ORDER BY ct DESC '''
    ),
    (
        '男女节目次数最多的男演员',
        '''SELECT m1.mid AS mid1, m1.name AS name1, COUNT(*) AS ct FROM program_own_with_stat AS p JOIN program_member AS pm1 ON p.pid = pm1.pid JOIN program_member AS pm2 ON pm1.pid = pm2.pid AND pm1.mid <> pm2.mid JOIN `member` AS m1 ON pm1.mid = m1.mid JOIN `member` AS m2 ON pm2.mid = m2.mid WHERE pm1.`position` < 4 AND pm2.`position` < 4 AND m1.gender = 'male' AND m2.gender = 'female' GROUP BY mid1 , name1 ORDER BY ct DESC , mid1 '''
    ),
    (
        '女搭档最多的男演员',
        '''SELECT m1.mid AS mid1, m1.name AS name1, COUNT(DISTINCT m2.mid) AS ct FROM program_own_with_stat AS p JOIN program_member AS pm1 ON p.pid = pm1.pid JOIN program_member AS pm2 ON pm1.pid = pm2.pid AND pm1.mid <> pm2.mid JOIN `member` AS m1 ON pm1.mid = m1.mid JOIN `member` AS m2 ON pm2.mid = m2.mid WHERE pm1.`position` < 4 AND pm2.`position` < 4 AND m1.gender = 'male' AND m2.gender = 'female' GROUP BY mid1 , name1 ORDER BY ct DESC , mid1 '''
    ),
    (
        '（本科）年级差距最大的搭档',
        '''SELECT mid1, m1.`name` AS name1, m1.grade_college, mid2, m2.`name` AS name2, m2.grade_college, diff FROM (SELECT pm1.mid AS mid1, pm2.mid AS mid2, COUNT(*) AS ct, ABS(pm2.grade_college - pm1.grade_college) AS diff FROM program_own_with_stat AS p JOIN all_program_member AS pm1 ON pm1.pid = p.pid AND pm1.position < 3 JOIN all_program_member AS pm2 ON pm2.pid = p.pid AND pm1.position < pm2.position AND pm2.position < 3 GROUP BY mid1 , mid2) AS c JOIN `member` AS m1 ON c.mid1 = m1.mid JOIN `member` AS m2 ON c.mid2 = m2.mid HAVING diff > 5 ORDER BY diff DESC , mid1 , mid2 '''
    ),
    (
        '捧哏不是第一次上台，视作老带新，统计老带新捧哏次数最多的人',
        '''DROP TABLE if exists m_first_dou; CREATE TEMPORARY TABLE m_first_dou SELECT pm.mid, pm.`name`, MIN(xueqi) xueqi_min, MIN(date) date_min FROM program_own_with_stat AS p JOIN all_program_member AS pm ON p.pid = pm.pid GROUP BY pm.mid , pm.name; DROP TABLE if exists m_first_peng; CREATE TEMPORARY TABLE m_first_peng SELECT pm.mid, pm.`name`, MIN(xueqi) xueqi_min, MIN(date) date_min FROM program_own_with_stat AS p JOIN all_program_member AS pm ON p.pid = pm.pid GROUP BY pm.mid , pm.`name`; SELECT m_peng.mid, m_peng.name AS peng_name, m_dou.name AS dou_name, p.date, p.show_name, p.program_name FROM program_own_with_stat AS p JOIN program_member AS pm_dou ON p.pid = pm_dou.pid AND pm_dou.position = 1 JOIN program_member AS pm_peng ON p.pid = pm_peng.pid AND pm_peng.position = 2 JOIN m_first_dou AS m_dou ON pm_dou.mid = m_dou.mid JOIN m_first_peng AS m_peng ON pm_peng.mid = m_peng.mid WHERE p.date > m_peng.date_min AND p.date = m_dou.date_min ORDER BY mid; '''
    ),
    (
        '攒底速度：所有攒过底的演员中，计算第一次攒底与第一次上台之间的距离(天数、专场数、个人节目数,三种指标)，并计算协会平均',
        '''SELECT m_first.mid, m_first.name, ROUND((xueqi_cuandi - xueqi_min) * 2) AS xueqi_delta, DATEDIFF(date_cuandi, date_min) AS date_delta, date_min, date_cuandi FROM (SELECT pm.mid, pm.name, MIN(xueqi) xueqi_min, MIN(date) date_min FROM program_own_with_stat AS p JOIN all_program_member AS pm ON p.pid = pm.pid GROUP BY pm.mid , pm.name) AS m_first JOIN (SELECT pm.mid, pm.name, MIN(xueqi) xueqi_cuandi, MIN(date) date_cuandi FROM program_own_with_stat AS p JOIN all_program_member AS pm ON p.pid = pm.pid WHERE pm.position < 4 AND p.sequence = p.max_sequence AND p.max_sequence > 3 GROUP BY pm.mid , pm.name) AS m_cuandi ON m_first.mid = m_cuandi.mid ORDER BY xueqi_delta , date_delta, date_cuandi '''
    )
)
