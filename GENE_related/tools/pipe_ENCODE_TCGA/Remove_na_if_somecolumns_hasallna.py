#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/TissuTypes/heatmaps/ENCODE_otherct_atleastBeta_0.5_MYtcga_all_matrix_folder_int_ENCODE_otherct_atleastBeta_0.5_all_matrix_allout_ranked_inflectionpos_sortedby_ENCODE_otherct_atleastBeta_0.5_all_matrix_allout_ranked_inflectionpos/ENCODE_otherct_atleastBeta_0.5_MYtcga_all_matrix_intwith_AdrenalGland_CpGdelta_info_faster.txt_5000_forheatunderlyingdata_ranked.txt_pos.txt_sorted.txt'
outfile=sys.argv[2] #'infile+"_nafixed.txt"
indf=pd.read_csv(infile,sep='\t')
indf.head()


# In[2]:


indf.columns


# In[3]:


outdf=indf.dropna(how='all',subset=['z_AdrenalGland_1a2ca9f7-d024-4996-9aa0-67f81655db9b.methylation_array.sesame.level3betas.txt_WGBS',
       'z_AdrenalGland_20aa2289-e9f9-4ffa-af6f-6e4dcd788e7b.methylation_array.sesame.level3betas.txt_WGBS',
       'z_AdrenalGland_25778e1f-592c-4de1-aaac-f395d5552e31.methylation_array.sesame.level3betas.txt_WGBS',
       'z_AdrenalGland_bc38f2ca-2253-4b89-8de3-224f5589a441.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Brain_07d27a99-baf0-4781-bd44-641303f93ead.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Brain_617785bf-02af-4d75-b7e6-1153c7d967f1.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Brain_c2cafa26-894b-4fe0-a287-3f7f067f8b01.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Brain_e10b0b3b-1d33-4812-863d-e045dc880b19.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Colorectal_0b240c58-ee45-4a81-b39c-feda560d6c8d.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Colorectal_154a802f-7a6b-4480-a7e3-663f724cfeb1.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Colorectal_55e32e08-3ea1-4a0c-9964-a3a563c2db4b.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Colorectal_6e89eb53-82f8-49a4-a29f-40df576ff2a0.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Esophagus_0a369dda-e325-40d7-817c-3f59c1a03f8b.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Esophagus_3404c2bd-31ab-4ab1-bc8d-cd904a9f4190.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Esophagus_91befd3f-8dae-4458-8345-1cef938dc750.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Esophagus_9755c0c3-0636-4110-a15d-56709317a571.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Heart_18dfa836-e8f5-4382-a59d-bbf10b21d5f9.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Heart_4f4fa8f0-fb9a-4862-9549-13f284c43ebe.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Heart_9a0d2933-32fa-45b3-931e-facd48f26f72.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Heart_d7cf04cb-8077-435d-96e9-83b7fa9e5294.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Liver_08787349-3ee0-4fe9-91f5-f97845844d69.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Liver_1faf9f76-ff29-4159-8e7b-2ff8129317c0.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Liver_5fd5b29b-a380-4908-af69-206c44572f7f.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Liver_c76b6b88-9f09-4388-9ff8-d39f27d3fd3f.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Lung_5a565ed8-f3c9-40d4-80ee-f8c756849037.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Lung_82aa5c8e-24e2-4ba0-83e7-6674b6f6b52d.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Lung_9da9edaf-f17c-4ba5-9872-661347778c9e.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Lung_af1c7d6b-f1d3-4abd-a5cd-b77b105a7a9e.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Ovary_1c336853-fe64-47d3-a47a-728442ca42b3.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Ovary_4a6814d1-7717-42aa-9947-10283b47d737.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Ovary_4cb4ae77-a981-4fa8-9b5a-1f838efed1ef.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Ovary_93604880-0222-48eb-8fb5-d230ff430923.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Pancreas_7d5db239-c6b9-4357-95ad-fbe088158e5b.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Pancreas_83109b70-f347-4468-bdbc-e169adb5d74a.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Pancreas_c7590713-7673-4818-8de3-1469f8937dc4.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Pancreas_fc979442-6743-465d-9739-68b2596eb7aa.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Prostate_1dde7bf5-fb08-463a-a6d4-64388d71054a.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Prostate_82fa329e-4440-4c91-b6d4-117adfb97c19.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Prostate_98c8c81d-8ab0-4d48-ae7f-8f57b1e1c208.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Prostate_d2bee562-2d51-417a-9fa5-adb87cfa7127.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Skin_59b22da8-32f6-44e2-876d-1e0e6b7d558a.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Skin_6069d9a9-28c8-44bd-9b36-292e0ab532f1.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Skin_875a9646-fef4-45ed-836b-123c2a9b0037.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Skin_c926225c-c168-4884-8e39-77ac13391ba7.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Stomach_008cf9de-d40d-4688-a2cd-b4c151250fc2.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Stomach_2e21525a-20a5-4b57-92df-d1c22c95a14a.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Stomach_45215be9-3e9f-4795-b539-a2c3c60fe350.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Stomach_a563fce7-624a-40f9-ada9-7a120ce4641d.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Testis_01f2edcb-e52c-4925-8494-0c1d7e2fb95c.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Testis_42c56370-f9d6-436d-b47e-5d6d50297152.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Testis_8c359ea9-e78a-4b71-9f12-a8099299aadd.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Testis_ef108754-e616-4a4e-aeea-f1460b86daef.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Thyroid_61c7d0e5-f83e-4a46-a508-14095a4be989.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Thyroid_996c6681-1e5e-4fa4-b043-1478ed144fa0.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Thyroid_a03ba478-2394-477b-82e4-0fc694fd159c.methylation_array.sesame.level3betas.txt_WGBS',
       'z_Thyroid_ce9f8c44-d2eb-48dc-9342-0c5c7e0ae54f.methylation_array.sesame.level3betas.txt_WGBS'])


# In[4]:


outdf.head()


# In[5]:


outdf.to_csv(outfile,sep='\t',index=False,na_rep='NA')

