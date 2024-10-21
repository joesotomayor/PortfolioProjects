-- Data Cleaning

-- 1. Edit the file from csv to json
UPDATE
    layoffs
SET
    company = CASE company WHEN 'None' THEN NULL ELSE company END,
    location = CASE location WHEN 'None' THEN NULL ELSE location END,
    industry = CASE industry WHEN 'None' THEN NULL ELSE industry END,
    total_laid_off = CASE total_laid_off WHEN 'None' THEN NULL ELSE total_laid_off END,
    percentage_laid_off = CASE percentage_laid_off WHEN 'None' THEN NULL ELSE percentage_laid_off END,
    date = CASE date WHEN 'None' THEN NULL ELSE date END,
    country = CASE country WHEN 'None' THEN NULL ELSE country END,
    funds_raised_millions = CASE funds_raised_millions WHEN 'None' THEN NULL ELSE funds_raised_millions END;
    
SELECT *
FROM layoffs;

ALTER TABLE layoffs
CHANGE COLUMN total_laid_off total_laid_off INT NULL DEFAULT NULL ,
CHANGE COLUMN funds_raised_millions funds_raised_millions INT NULL DEFAULT NULL ;

-- 2. Remove Duplicates

-- Create a second table, in that way we don't modify the raw data
CREATE TABLE layoffs_staging
LIKE layoffs;

INSERT layoffs_staging
SELECT *
FROM layoffs;

SELECT * ,
ROW_NUMBER() OVER(
PARTITION BY company, industry, total_laid_off, percentage_laid_off, `date`) AS row_num
FROM layoffs_staging;

-- CTE

WITH duplicate_cte AS
(
SELECT * ,
ROW_NUMBER() OVER(
PARTITION BY company, location,
industry, total_laid_off, percentage_laid_off, `date`, stage,
country, funds_raised_millions) AS row_num
FROM layoffs_staging
)
SELECT * 
FROM duplicate_cte
WHERE row_num > 1;

-- Check duplicates
SELECT *
FROM layoffs_staging
WHERE company = 'Cazoo';

-- Creating a third table to eliminate duplicates

CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num` INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SELECT *
FROM layoffs_staging2
WHERE row_num > 1;

INSERT INTO layoffs_staging2
SELECT *,
ROW_NUMBER() OVER(
PARTITION BY company, location,
industry, total_laid_off, percentage_laid_off, `date`, stage,
country, funds_raised_millions) AS row_num
FROM layoffs_staging;

DELETE
FROM layoffs_staging2
WHERE row_num > 1;

SELECT *
FROM layoffs_staging2;

-- 3. Standardizing data

-- Eliminate white spaces

UPDATE layoffs_staging2
SET company = TRIM(company);

-- Convert Crypto Currency into Crypto 

SELECT DISTINCT industry
FROM layoffs_staging2
ORDER BY 1;

UPDATE layoffs_staging2
SET industry = 'Crypto'
WHERE industry LIKE 'Crypto%';

-- Convert United States. to United States

SELECT DISTINCT country
FROM layoffs_staging2
ORDER BY 1;

SELECT DISTINCT country, TRIM(TRAILING '.' FROM country)
FROM layoffs_staging2
ORDER BY 1;

UPDATE layoffs_staging2
SET country = TRIM(TRAILING '.' FROM country)
WHERE country LIKE 'United States%';

-- Standard Date format

SELECT `date`
FROM layoffs_staging2;

UPDATE layoffs_staging2
SET `date` = STR_TO_DATE(`date`, '%m/%d/%Y');

ALTER TABLE layoffs_staging2
MODIFY COLUMN `date` DATE; 

-- 4. Null Values or blank values

SELECT *
FROM layoffs_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

SELECT *
FROM layoffs_staging2
WHERE industry IS NULL
OR industry = '';

SELECT *
FROM layoffs_staging2
WHERE company = 'Airbnb';

-- Update the blank spaces for NULL values

UPDATE layoffs_staging2
SET industry = NULL
WHERE industry = '';

-- Update with a non blank value

SELECT t1.industry, t2.industry
FROM layoffs_staging2 t1
JOIN layoffs_staging2 t2
   ON t1.company = t2.company
WHERE t1.industry IS NULL
AND t2.industry IS NOT NULL;

UPDATE layoffs_staging2 t1
JOIN layoffs_staging2 t2
   ON t1.company = t2.company
SET t1.industry = t2.industry
WHERE t1.industry IS NULL
AND t2.industry IS NOT NULL;

-- 5. Remove Any Columns or Rows

SELECT *
FROM layoffs_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

DELETE
FROM layoffs_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

ALTER TABLE layoffs_staging2
DROP COLUMN row_num;










