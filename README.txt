

If we have a file of the same checksum, use the first one we find, with the artist & album


If we have the same artist, album and filename with a different checksum,
            Create a new album to host the file
            Create a new file name



What do we do with non MP3 files?
    Write another scanner....




    ﻿-- Licensed Materials - Property of IBM
-- sqlRights.sql
-- (c) Copyright IBM Corporation 2004, 2008.  All Rights Reserved.
-- U.S. Government Users Restricted Rights:  Use, duplication or disclosure
-- restricted by GSA ADP Schedule Contract with IBM Corp.

-- ===========================================================================
-- Create a role with the necessary grants for a standard SA user
-- ===========================================================================

BEGIN
	--Declares
	DECLARE @id int,
	@Name nvarchar(50),
	@Grant nvarchar(200),
	@output nvarchar(max)

	SET @output = ''
	--Drop tmpTable if it exists
	IF EXISTS(SELECT Name FROM tempdb..sysobjects WHERE name LIKE '#tmpRightsTable%')
		DROP TABLE #tmpRightsTable

	--Create temp table
	CREATE TABLE #tmpRightsTable
	(
		ID int IDENTITY(1,1) NOT NULL,
		Name nvarchar(50),
		Grants nvarchar(200),
		xType nvarchar(5)
	)
	--Check to see if the SAUser role exists
	IF (NOT EXISTS (SELECT Name FROM sys.database_principals WHERE UPPER(Name) = UPPER('SAUser')))
		exec sp_AddRole N'SAUser'

	-- Insert procedures into tmpTable
	INSERT INTO #tmpRightsTable (Name, Grants, xType)
	SELECT o.name, case when (xType = 'TF' OR xType = 'IF') then 'SELECT' else 'EXECUTE' end, xtype from dbo.sysobjects o join sys.all_objects syso on o.id = syso.object_id where xtype in ('P', 'X', 'RF', 'TF', 'FN', 'IF') and o.name not like N'#%%' AND category NOT IN  (2) order by o.name

	-- Insert Tables into tmpTable
	INSERT INTO #tmpRightsTable (Name, Grants, xType)
	SELECT o.name, case when OBJECTPROPERTY(o.id, N'IsView') = 1 then 'SELECT' ELSE 'SELECT, INSERT, UPDATE, DELETE' END, case when OBJECTPROPERTY(o.id, N'IsView') = 1 then 'VU' ELSE 'TBL' END  from dbo.sysobjects o join sys.all_objects syso on o.id = syso.object_id where (OBJECTPROPERTY(o.id, N'IsView') = 1 OR OBJECTPROPERTY(o.id, N'IsTable') = 1) and o.name not like N'#%%' and is_ms_shipped = 0  order by o.name

	--Grant rights to SAUser
	SET ROWCOUNT 1
	SELECT @id = ID, @Name = Name, @Grant = Grants FROM #tmpRightsTable

	WHILE @@ROWCOUNT <> 0
		BEGIN
			SET ROWCOUNT 0
			SET @output = @output + CHAR(13) + ' GRANT ' + @Grant + ' ON ' + @Name + ' TO SAUser'
			DELETE #tmpRightsTable WHERE ID = @id

			SET ROWCOUNT 1
			SELECT @id = ID, @Name = Name, @Grant = Grants FROM #tmpRightsTable
		END

	SET ROWCOUNT 0

	exec SP_EXECUTESQL @output

	--Drop tmpTable if it exists
	IF EXISTS(SELECT Name FROM tempdb..sysobjects WHERE name LIKE '#tmpRightsTable%')
		DROP TABLE #tmpRightsTable

END



