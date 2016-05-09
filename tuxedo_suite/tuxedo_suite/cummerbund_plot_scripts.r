
library(cummeRbund)

#load cuff_diff_out files for plotting
cuff = readCufflinks('cuff_diff_out')


#make a density plot and save it can be pdf(), jpeg(), png()
png('./r_plots/density_plot.png', width = 2000, height = 1500, res = 300)
csDensity(genes(cuff))
dev.off()

png('./r_plots/scatter_matrix_plot.png', width = 2000, height = 1500, res = 300)
csScatterMatrix(genes(cuff))
dev.off()

png('./r_plots/volcano_matrix_plot.png', width = 2000, height = 1500, res = 300)
csVolcanoMatrix(genes(cuff))
dev.off()


gene_diff_data	=	diffData(genes(cuff))
sig_gene_data	=	subset(gene_diff_data,(significant=='yes'	|	p_value	<	0.01))
write.table(sig_gene_data,'./r_plots/sig_diff_genes.txt', sep = '\t', quote=F)


sig_genes=getGenes(cuff,sig_gene_data$gene_id)
png('./r_plots/heat_map_significant_de_genes.png', width = 2000, height = 1500, res = 300)
csHeatmap(sig_genes,cluster='both')
dev.off()
