%% Batch compression of nc files to zip files
% path1:Path where the nc file is located
% path2:Path where the zip file will be placed
input_dir=path1;
fileFolder=fullfile(input_dir);
dir_input=dir(fullfile(fileFolder,'*.nc'));
file_Names=sort_nat({dir_input.name}');
image_num=length(file_Names);

data_name_year = string(cellfun(@(x) x(7:10),file_Names,'UniformOutput',false));
year_unique=unique(data_name_year);

for i=1:size(year_unique,1)
    [a,b]=find(data_name_year==year_unique(i));
    filesToZip = {};
    for j=1:size(a,1)
        filesToZip(j)=cellstr([input_dir,file_Names{j}]);
    end
    zip([path2,char(year_unique(i)),'.zip'], filesToZip);
end