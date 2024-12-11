-- Procedure lấy thông tin config --

DELIMITER //

CREATE PROCEDURE GetConfig(IN configId BIGINT)
BEGIN
    SELECT * FROM configs WHERE id = configId AND flag = true;
END //

DELIMITER ;

-- Procedure lấy thông tin resource ---

DELIMITER //
CREATE PROCEDURE GetResource(IN resourceId INT)
BEGIN
    SELECT * FROM resources WHERE id = resourceId;
END //

DELIMITER ;

-- Procedure thêm thông tin log ---

DELIMITER //
CREATE PROCEDURE InsertLog(
    IN configId BIGINT,
    IN fileName VARCHAR(255),
    IN fileSize DOUBLE,
    IN recordsCount INT,
    IN msg VARCHAR(255),
    IN processId INT
)
BEGIN
    INSERT INTO logs (config_id, file_name, file_size, records_count, process_id, message, created_at)
        VALUES (configId, fileName, fileSize, recordsCount, processId, msg, NOW()) ;
END //

DELIMITER ;

-- Procedure cập nhật thông tin log ---

DELIMITER //
CREATE PROCEDURE UpdateLog(
    IN logId BIGINT,
    IN msg VARCHAR(255),
    IN processId INT
)
BEGIN
    UPDATE logs SET message = msg, process_id = processId, updated_at = NOW() WHERE id = logId;
END //

-- Procedure lấy thông tin log --

DELIMITER //
CREATE PROCEDURE GetLog(
    IN configId BIGINT,
    IN processId INT,
    IN date DATE
)
BEGIN
    SELECT * FROM logs WHERE config_id = configId AND process_id = processId AND DATE(created_at) = date;
END //

DELIMITER ;
