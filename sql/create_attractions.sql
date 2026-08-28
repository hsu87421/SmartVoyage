-- 景点数据表
CREATE TABLE IF NOT EXISTS attractions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键，自增，唯一标识每条记录',
    name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '景点名称，如"故宫"',
    province VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '省份，如"北京"',
    city VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '城市，如"北京"',
    district VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '区域，如"东城区"',
    address VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '详细地址',
    category VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '景点类别，如"历史文化"、"自然风景"、"主题乐园"、"美食"',
    description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '景点描述',
    opening_hours VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '开放时间，如"09:00-17:00"',
    ticket_price DECIMAL(10, 2) COMMENT '门票价格',
    rating DECIMAL(3, 2) COMMENT '评分，1-5分',
    visit_duration_min INT COMMENT '建议游览时间（分钟）',
    visit_duration_max INT COMMENT '建议游览时间（分钟）',
    is_free BOOLEAN DEFAULT FALSE COMMENT '是否免费',
    suitable_season VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '最佳游览季节',
    accessibility VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '交通方式，如"地铁1号线"',
    tips TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '游览提示和注意事项',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY unique_attraction (city, name),
    INDEX idx_city (city),
    INDEX idx_category (category),
    INDEX idx_rating (rating)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='景点信息表';


-- 插入示例数据 - 北京
INSERT INTO attractions (name, province, city, district, address, category, description, opening_hours, ticket_price, rating, visit_duration_min, visit_duration_max, is_free, suitable_season, accessibility, tips) 
VALUES 
('故宫', '北京', '北京', '东城区', '北京市东城区景山前街4号', '历史文化', '中国明清两代的皇家宫殿，是古代宫廷建筑的杰作', '09:00-17:00', 60.00, 4.8, 180, 360, FALSE, '春秋季节', '地铁1号线天安门东站', '提前预约购票，避免高峰时段'),
('长城', '北京', '北京', '延庆区', '北京市延庆区八达岭镇军都山关沟古道北口', '自然风景', '世界文化遗产，中国古代防御工事的代表', '07:00-18:00', 40.00, 4.7, 240, 480, FALSE, '春秋季节', '八达岭高铁站直达', '登山较累，穿舒适的登山鞋'),
('天坛', '北京', '北京', '东城区', '北京市东城区天坛路1号', '历史文化', '世界现存最大的祭祀性古建筑群', '08:00-17:00', 35.00, 4.5, 120, 240, FALSE, '春夏秋季', '地铁5号线天坛东门站', '北侧有厚重的历史气息，推荐早上游览'),
('颐和园', '北京', '北京', '海淀区', '北京市海淀区新建宫门路19号', '皇家园林', '皇家园林博物馆，融山水园林与宫廷建筑于一体', '06:30-18:00', 30.00, 4.6, 180, 360, FALSE, '春秋季节', '地铁4号线北宫门站', '园区很大，建议租赁电瓶车游览'),
('北京动物园', '北京', '北京', '西城区', '北京市西城区西直门外大街137号', '主题乐园', '中国开放最早，建园最早的动物园', '07:30-18:00', 15.00, 4.2, 180, 360, FALSE, '春秋季节', '地铁4号线动物园站', '分区游览，建议先看掠食动物表演');

-- 插入示例数据 - 上海
INSERT INTO attractions (name, province, city, district, address, category, description, opening_hours, ticket_price, rating, visit_duration_min, visit_duration_max, is_free, suitable_season, accessibility, tips) 
VALUES 
('外滩', '上海', '上海', '黄浦区', '上海市黄浦区中山东一路', '历史文化', '上海的象征，汇集了各国建筑风格的万国建筑博览群', '全天', 0.00, 4.7, 60, 180, TRUE, '全年', '地铁2号线南京东路站', '夜景特别美，建议傍晚去'),
('东方明珠电视塔', '上海', '上海', '浦东新区', '上海市浦东新区世纪大道1号', '现代建筑', '亚洲第二高的塔，登顶可俯瞰上海全景', '08:00-21:00', 150.00, 4.5, 120, 240, FALSE, '全年', '地铁2号线陆家嘴站', '购票时选择电子票，避免排队'),
('城隍庙', '上海', '上海', '黄浦区', '上海市黄浦区方浜中路249号', '历史文化', '上海道教宫观，古代建筑艺术的精品', '08:30-16:30', 10.00, 4.3, 60, 120, FALSE, '全年', '地铁10号线豫园站', '古镇小吃众多，可一并品尝'),
('南京路步行街', '上海', '上海', '黄浦区', '上海市黄浦区南京东路', '美食购物', '中国最著名的商业街，汇集国内外一线品牌', '全天', 0.00, 4.4, 120, 240, TRUE, '全年', '地铁1号线、2号线南京东路站', '人很多，建议避开周末和节假日'),
('迪士尼乐园', '上海', '上海', '浦东新区', '上海市浦东新区川沙新镇黄赵路310号', '主题乐园', '亚洲最大的迪士尼度假区', '08:00-22:00', 385.00, 4.6, 480, 600, FALSE, '全年', '地铁11号线迪士尼站', '建议多日游，一天内可能无法游遍');

-- 插入示例数据 - 杭州
INSERT INTO attractions (name, province, city, district, address, category, description, opening_hours, ticket_price, rating, visit_duration_min, visit_duration_max, is_free, suitable_season, accessibility, tips) 
VALUES 
('西湖', '浙江', '杭州', '西湖区', '杭州市西湖风景名胜区', '自然风景', '中国十大风景名胜之一，因诗人苏轼而得名', '全天', 0.00, 4.8, 180, 360, TRUE, '春秋季节', '地铁1号线龙翔桥站', '环湖路线长，建议骑单车游览'),
('灵隐寺', '浙江', '杭州', '西湖区', '杭州市西湖区法云路15号', '历史文化', '中国著名佛刹，有"江南禅寺"之称', '07:00-18:00', 30.00, 4.5, 120, 240, FALSE, '全年', '公交车Y2线', '寺院肃静，来访请尊重宗教信仰'),
('西溪湿地', '浙江', '杭州', '余杭区', '杭州市余杭区西溪路洪园路西溪湿地公园', '自然风景', '国内首个都市湿地公园，素有"城市绿肺"之称', '09:00-17:00', 120.00, 4.4, 240, 360, FALSE, '春秋季节', '地铁1号线西溪湿地站', '划船游览更有意思，另收费'),
('千岛湖', '浙江', '杭州', '淳安县', '浙江省杭州市淳安县千岛湖风景名胜区', '自然风景', '人工湖，因湖中有1078个岛屿而得名', '08:00-17:00', 150.00, 4.6, 480, 720, FALSE, '春秋季节', '杭州中心客运站有班车', '距杭州较远，建议多留时间');

-- 创建景点评价表（可选）
CREATE TABLE IF NOT EXISTS attraction_reviews (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '评价ID',
    attraction_id INT NOT NULL COMMENT '景点ID',
    user_name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '用户名',
    rating INT COMMENT '评分，1-5',
    review_text TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '评价内容',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (attraction_id) REFERENCES attractions(id),
    INDEX idx_attraction_id (attraction_id)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='景点评价表';

-- 创建用户偏好表（可选）
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '偏好ID',
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    preferred_categories VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '偏好类别，多个用逗号分隔',
    preferred_cities VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '偏好城市，多个用逗号分隔',
    min_rating DECIMAL(3, 2) COMMENT '最低评分要求',
    max_price DECIMAL(10, 2) COMMENT '最高价格',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY unique_user (user_id),
    INDEX idx_user_id (user_id)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户偏好表';
