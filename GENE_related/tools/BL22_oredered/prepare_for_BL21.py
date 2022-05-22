#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/B22withLTME/v3_3steps/thirdstepanalysis/try3/towardsSM/heatmaps/preparefrom_patient_pbl/test/BL22LTME_patientPBL_all_matrix_intwith_naive_myloid_CD8TIL_OthermeanIINTWITH_melCD8TIL_activatted-.1_intwith_CD8TL_melCD8TIL_-0.7CD8TIL_-0.7_onlypos'
outfile=sys.argv[2]   #infile+"_ready.txt"


indf=pd.read_csv(infile,sep="\t")
indf.head()


# In[2]:


colincluded=['chrom','start','end','aS007DD51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-naive-CD4-T-cell.bw.bedgraph_rolled','aS007G756.CPG_methylation_calls.bs_call.GRCh38.20160531-P-naive-CD4-T-cell.bw.bedgraph_rolled','aS009W451.CPG_methylation_calls.bs_call.GRCh38.20160531-P-naive-CD4-T-cell.bw.bedgraph_rolled','sS001U352.CPG_methylation_calls.bs_call.GRCh38.20160531-P-EM-CD4pos_T-cell.bw.bedgraph_rolled','sS014QS51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-EM-CD4pos_T-cell.bw.bedgraph_rolled','vS006YC51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-CM-CD4pos_T-cell.bw.bedgraph_rolled','vS014QS55.CPG_methylation_calls.bs_call.GRCh38.20160531-P-CM-CD4pos_T-cell.bw.bedgraph_rolled','rS001U353.CPG_methylation_calls.bs_call.GRCh38.20160531-P-Tregs.bw.bedgraph_rolled','rS00XTP51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-Tregs.bw.bedgraph_rolled','bC00256A1bs.CPG_methylation_calls.bs_call.GRCh38.20160531-P-naive-CD8-T-cell.bw.bedgraph_rolled','bC003VO55.CPG_methylation_calls.bs_call.GRCh38.20160531-P-naive-CD8-T-cell.bw.bedgraph_rolled','bC0066P51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-naive-CD8-T-cell.bw.bedgraph_rolled','oC00256A3bs.CPG_methylation_calls.bs_call.GRCh38.20160531-P-EM-CD8pos_T-cell.bw.bedgraph_rolled','oS014WG51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-EM-CD8pos_T-cell.bw.bedgraph_rolled','nC003VO56.CPG_methylation_calls.bs_call.GRCh38.20160531-P-CM-CD8pos_T-cell.bw.bedgraph_rolled','nC005UI52.CPG_methylation_calls.bs_call.GRCh38.20160531-P-CM-CD8pos_T-cell.bw.bedgraph_rolled','tS002ND51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-EM-CD8pos_T-cell_term-diff.bw.bedgraph_rolled','tS0164R51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-EM-CD8pos_T-cell_term-diff.bw.bedgraph_rolled','dC002CTA1bs.CPG_methylation_calls.bs_call.GRCh38.20160531-P-NK_cell.bw.bedgraph_rolled','dC0067N51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-NK_cell.bw.bedgraph_rolled','dS01E8O51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-NK_cell.bw.bedgraph_rolled','cC0068L51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-naive_B_cell.bw.bedgraph_rolled','cNBC_NC11_41.CPG_methylation_calls.bs_call.GRCh38.20160531-P-naive_B_cell.bw.bedgraph_rolled','cS01ECGA1.CPG_methylation_calls.bs_call.GRCh38.20160531-P-naive_B_cell.bw.bedgraph_rolled','xC003N351.CPG_methylation_calls.bs_call.GRCh38.20160531-P-memory_B_cell.bw.bedgraph_rolled','xS017RE51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-memory_B_cell.bw.bedgraph_rolled','fS01BHIA1.CPG_methylation_calls.bs_call.GRCh38.20160531-P-CD14pos_classical_monocyte.bw.bedgraph_rolled','fS01E03A1.CPG_methylation_calls.bs_call.GRCh38.20160531-P-CD14pos_classical_monocyte.bw.bedgraph_rolled','fS01MAPA1.CPG_methylation_calls.bs_call.GRCh38.20160531-P-CD14pos_classical_monocyte.bw.bedgraph_rolled','gS001S751.CPG_methylation_calls.bs_call.GRCh38.20160531-P-macrophage_M0.bw.bedgraph_rolled','gS0022I51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-macrophage_M0.bw.bedgraph_rolled','gS0039051.CPG_methylation_calls.bs_call.GRCh38.20160531-P-macrophage_M0.bw.bedgraph_rolled','hS001S753.CPG_methylation_calls.bs_call.GRCh38.20160531-P-Inflammatory_macrophage_M1.bw.bedgraph_rolled','hS0022I53.CPG_methylation_calls.bs_call.GRCh38.20160531-P-Inflammatory_macrophage_M1.bw.bedgraph_rolled','hS00H6O51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-Inflammatory_macrophage_M1.bw.bedgraph_rolled','iS0062252.CPG_methylation_calls.bs_call.GRCh38.20160531-P-alt_activated_macrophage_M2.bw.bedgraph_rolled','iS00E8W51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-alt_activated_macrophage_M2.bw.bedgraph_rolled','iS00FTN51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-alt_activated_macrophage_M2.bw.bedgraph_rolled','jS00TU2A1.CPG_methylation_calls.bs_call.GRCh38.20160531-P-immature_conventional_dendritic_cell.bw.bedgraph_rolled','jS00TV0A1.CPG_methylation_calls.bs_call.GRCh38.20160531-P-immature_conventional_dendritic_cell.bw.bedgraph_rolled','kS00TXXA1.CPG_methylation_calls.bs_call.GRCh38.20160531-P-mature_conventional_dendritic_cell.bw.bedgraph_rolled','kS00TYVA1.CPG_methylation_calls.bs_call.GRCh38.20160531-P-mature_conventional_dendritic_cell.bw.bedgraph_rolled','lC000S5A2bs.CPG_methylation_calls.bs_call.GRCh38.20160531-P-mature_neutrophils.bw.bedgraph_rolled','lC0010KA1bs.CPG_methylation_calls.bs_call.GRCh38.20160531-P-mature_neutrophils.bw.bedgraph_rolled','lC001UYA1bs.CPG_methylation_calls.bs_call.GRCh38.20160531-P-mature_neutrophils.bw.bedgraph_rolled','uS004AV51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-megakaryocyte.bw.bedgraph_rolled','uS004BT51.CPG_methylation_calls.bs_call.GRCh38.20160531-P-megakaryocyte.bw.bedgraph_rolled','qS006XE53.CPG_methylation_calls.bs_call.GRCh38.20160531-P-mature-eosinophil.bw.bedgraph_rolled','qS00V6553.CPG_methylation_calls.bs_call.GRCh38.20160531-P-mature-eosinophil.bw.bedgraph_rolled','wS002R551.CPG_methylation_calls.bs_call.GRCh38.20160531-P-Erythroblast.bw.bedgraph_rolled','wS002S351.CPG_methylation_calls.bs_call.GRCh38.20160531-P-Erythroblast.bw.bedgraph_rolled']

outdf=indf[colincluded]

#outdf=indf.drop(['ymel-1254-T-CD14.bedgraph_rolled','ymel-1254-T-CD4.bedgraph_rolled','ymel-1457-T-CD14.bedgraph_rolled','ymel-1457-T-CD4.bedgraph_rolled','ymel-960-T-CD14.bedgraph_rolled','ymel-960-T-CD4.bedgraph_rolled'],axis=1)


# In[3]:


outdf.to_csv(outfile,sep="\t",na_rep="NA",index=False)

