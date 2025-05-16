%% make station list for spatial-based 10-fold valification
% path1:The path to the mat file where the station location is stored
% path2:The path where the validation station location will be placed
% path3:The path where the training station location will be placed
xy=importdata(path1);
spital_unique=unique(xy,'rows','stable')';
spital_unique=spital_unique';
rowrank = randperm(size(spital_unique, 1));
spital_unique = spital_unique(rowrank,:);
one_fold_num=ceil(size(spital_unique,1)/10);

for fold=1:10
    fold
    if fold~=10
        spital_va=spital_unique((one_fold_num*(fold-1)+1):one_fold_num*fold,:);
    else
        spital_va=spital_unique((one_fold_num*(fold-1)+1):end,:);
    end
    spatial_tra=setdiff(spital_unique,spital_va,'rows');
    save([path2,num2str(fold,'%02d'),'.mat'],'spital_va')
    save([path3,num2str(fold,'%02d'),'.mat'],'spatial_tra')
end