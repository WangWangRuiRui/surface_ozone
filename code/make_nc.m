%% Convert mat data to nc file
% path1:Path where the mat file is located
% path2:Path where the nc file will be placed

input_dir=path1;
fileFolder=fullfile(input_dir);
dir_input=dir(fullfile(fileFolder,'*.mat'));
file_Names=sort_nat({dir_input.name}');
image_num=length(file_Names);

for i=1:image_num
    data=importdata(strcat(input_dir,file_Names{i}));
    [latSize, lonSize] = size(data);
    lat = linspace(-90, 90, latSize);
    lat = flip(lat,2);
    lon = linspace(-180, 180, lonSize);
    ncid = netcdf.create([path2,file_Names{i}(1:8),'.nc'],'NC_NOCLOBBER');
    dimidx = netcdf.defDim(ncid,'latitude',length(lat));
    dimidy = netcdf.defDim(ncid,'longitude',length(lon));
    ncVarLat = netcdf.defVar(ncid, 'latitude', 'float', dimidx);
    ncVarLon = netcdf.defVar(ncid, 'longitude', 'float', dimidy);
    varid = netcdf.defVar(ncid,'O3','float',[dimidx dimidy]);
    netcdf.putAtt(ncid, ncVarLat, 'units', 'degrees_north');
    netcdf.putAtt(ncid, ncVarLon, 'units', 'degrees_east');
    netcdf.putAtt(ncid, varid, 'units', 'μg/m³'); 
    netcdf.endDef(ncid)
    netcdf.putVar(ncid, ncVarLat, lat);
    netcdf.putVar(ncid, ncVarLon, lon);
    netcdf.putVar(ncid,varid,data)
    netcdf.close(ncid);
end
