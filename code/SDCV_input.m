%% SDCV valification
% path1:The path where the training data is located
% path2:The path where the location of the training data in the study area is located
% path3:The path where the location of the validation data in the study area is located
% path4:The path where the training data processed by the SDCV method will be placed

train_data=importdata(path1);
train_xy=importdata(path2);
va_xy=importdata(path3);
va_xy=unique(va_xy,'rows');
for d=1:20
    train_d=train_data;
    point_remove_all=[];
    for pos=1:size(va_xy,1)
        y=train_xy(:,1)-va_xy(pos,1);
        x=train_xy(:,2)-va_xy(pos,2);
        x=abs(x);
        x(find(x>1800))=3600-x(find(x>1800));
        distance=sqrt(y.*y+x.*x);
        point_remove=find(distance<=d);
        point_remove_all=[point_remove_all;point_remove];
    end
    point_remove_all=unique(point_remove_all);
    train_d(point_remove_all,:)=[];
    save(path4,'train_d')
end