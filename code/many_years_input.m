%% Split multi-year input data based on the list of station locations
% path1:The path to the mat file where the station location is stored
% path2:The path where the validation station location will be placed
% path3:The path where the multi-year input data is stored
% path4:The path where the splitted training data will be placed
% path5:The path where the splitted validation data will be placed

input_dir_va=path1;
fileFolder_va=fullfile(input_dir_va);
dir_input_va=dir(fullfile(fileFolder_va,'*.mat'));
file_Names_va=sort_nat({dir_input_va.name}');
image_num=length(file_Names_va);

input_dir_tra=path2;
fileFolder_tra=fullfile(input_dir_tra);
dir_input_tra=dir(fullfile(fileFolder_tra,'*.mat'));
file_Names_tra=sort_nat({dir_input_tra.name}');

input_dir_data=path3;
fileFolder_data=fullfile(input_dir_data);
dir_input_data=dir(fullfile(fileFolder_data,'*.mat'));
file_Names_data=sort_nat({dir_input_data.name}');

for i=1:size(year_list,2)
    i
    y=char(year_list(i));
    data=importdata(strcat(input_dir_data,file_Names_data{i}));
    for j=1:10
        spital_va=importdata(strcat(input_dir_va,file_Names_va{j}));
        spatial_tra=importdata(strcat(input_dir_tra,file_Names_tra{j}));
        
        % Columns 32 and 33 of data indicate the geographic location
        [isva,pos]=ismember(data(:,32:33),spital_va, 'rows');
        [isva_row,isva_col]=find(isva==1);
        va_data=data(isva_row,:);
        [istra,pos]=ismember(data(:,32:33),spatial_tra, 'rows');
        [istra_row,istra_col]=find(istra==1);
        tra_data=data(istra_row,:);
        
        save([path4,'train_',num2str(j,'%02d'),'_',file_Names_tra{i}],'tra_data')
        save([path5,num2str(j,'%02d'),'.mat'],'va_data')
    end
end