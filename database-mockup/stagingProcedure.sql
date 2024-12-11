-- Procedure transform temporary sang daily của kyma resource --

DELIMITER //

CREATE PROCEDURE TransformTemporaryIntoDailyKM(IN date DATE)
BEGIN
    INSERT IGNORE INTO daily_kyma_cameras (
        id,
        name,
        link,
        regular_price,
        discounted_price,
        brand,
        images,
        warranty,
        origin,
        date,
        color_texts,
        color_pics,
        date_sk
    )
    SELECT
        id,
        name,
        link,
        CAST(REPLACE(REPLACE(SUBSTRING_INDEX(regular_price, ' ', 1), ',', ''), 'VNĐ', '') AS DOUBLE) AS regular_price,
        CAST(REPLACE(REPLACE(SUBSTRING_INDEX(discounted_price, ' ', 1), ',', ''), 'VNĐ', '') AS DOUBLE) AS discounted_price,
        brand,
        images,
        IFNULL(NULLIF(warranty, ''), 'Không xác định') AS warranty,
        IFNULL(NULLIF(origin, ''), 'Không xác định') AS origin,
        STR_TO_DATE(date, '%Y-%m-%d'),
        IFNULL(NULLIF(color_texts, ''), 'Không xác định') AS color_texts,
        IFNULL(NULLIF(color_pics, ''), 'Không xác định') AS color_pics,
        (SELECT date_dim.sk FROM date_dim WHERE date_dim.calendar_date = date)
    FROM temp_kyma_cameras;
END //

DELIMITER ;

-- Procedure transform temporary sang daily của binh minh digital resource --

DELIMITER //

CREATE PROCEDURE TransformTemporaryIntoDailyBMD(IN date DATE)
BEGIN
    INSERT INTO daily_bmd_cameras (
        id,
        name,
        quantity_in_stock,
        link,
        regular_price,
        discounted_price,
        brand,
        images,
        warranty,
        origin,
        date,
        color_texts,
        color_pics,
        date_sk
    )
    SELECT
        id,
        name,
        CASE
            WHEN quantity_in_stock LIKE '% sản phẩm' THEN CAST(SUBSTRING_INDEX(quantity_in_stock, ' ', 1) AS UNSIGNED)
            WHEN LOWER(quantity_in_stock) = 'hết hàng' THEN 0
        END,
        link,
        CASE
            WHEN regular_price LIKE 'Liên hệ%' THEN 100
            ELSE CAST(REPLACE(REPLACE(SUBSTRING_INDEX(regular_price, ' ', 1), ',', ''), 'VNĐ', '') AS DOUBLE)
        END,
        CASE
            WHEN discounted_price LIKE 'Liên hệ%' THEN 100
            ELSE CAST(REPLACE(REPLACE(SUBSTRING_INDEX(discounted_price, ' ', 1), ',', ''), 'VNĐ', '') AS DOUBLE)
        END,
        brand,
        images,
        IFNULL(NULLIF(warranty, ''), 'Không xác định') AS warranty,
        IFNULL(NULLIF(origin, ''), 'Không xác định') AS origin,
        STR_TO_DATE(date, '%Y-%m-%d'),
        IFNULL(NULLIF(color_texts, ''), 'Không xác định') AS color_texts,
        IFNULL(NULLIF(color_pics, ''), 'Không xác định') AS color_pics,
        (SELECT date_dim.sk FROM date_dim WHERE date_dim.calendar_date = date)
    FROM temp_bmd_cameras;
END //

DELIMITER ;