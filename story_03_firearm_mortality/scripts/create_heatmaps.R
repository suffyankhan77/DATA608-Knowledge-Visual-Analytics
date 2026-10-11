# Story 3: Do stricter gun laws reduce firearm gun deaths?
#**Muhammad Suffyan Khan · DATA 608 · Fall 2026**

dat <- read.csv("data/processed/state_analysis_2024.csv", stringsAsFactors = FALSE)
stopifnot(nrow(dat) == 50, length(unique(dat$abbr)) == 50,
          all(dat$law_level %in% 1:5), all(is.finite(dat$firearm_death_rate_2024)))

# A stylized 50-state tile cartogram. Position suggests broad geography; area
# and adjacency do not match geographic state boundaries. AK and HI are insets.
tiles <- data.frame(abbr=c(
  "ME", "WA","MT","ND","MN","WI","MI","VT","NH",
  "OR","ID","SD","IA","IL","IN","OH","PA","NY","MA",
  "CA","NV","WY","NE","MO","KY","WV","VA","MD","NJ","CT","RI",
  "AZ","UT","CO","KS","AR","TN","NC","SC","DE",
  "NM","OK","LA","MS","AL","GA","FL",
  "TX","AK","HI"),
  col=c(12,2,3,4,5,6,7,10,11, 2,3,4,5,6,7,8,9,10,11,
        1,2,3,4,5,6,7,8,9,10,11,12, 2,3,4,5,6,7,8,9,10,
        3,4,5,6,7,8,9, 4,1,2),
  row=c(1,2,2,2,2,2,2,2,2, 3,3,3,3,3,3,3,3,3,3,
        4,4,4,4,4,4,4,4,4,4,4,4, 5,5,5,5,5,5,5,5,5,
        6,6,6,6,6,6,6, 7,8,8))
stopifnot(length(unique(tiles$abbr))==50,
          !anyDuplicated(paste(tiles$row,tiles$col)),
          setequal(tiles$abbr,dat$abbr))
tiles <- merge(tiles,dat,by="abbr",sort=FALSE)
colors <- grDevices::hcl.colors(5,"Viridis")
rate_colors <- grDevices::hcl.colors(128,"Viridis")
rate_max <- 30 # fixed 0-30 rates per 100,000; no sample-relative rescaling

# WCAG relative luminance: choose whichever text color has higher contrast.
readable <- function(bg) {
  rgb <- grDevices::col2rgb(bg)[,1]/255
  lin <- ifelse(rgb <= .04045, rgb/12.92, ((rgb+.055)/1.055)^2.4)
  lum <- sum(lin*c(.2126,.7152,.0722))
  if ((lum+.05)/.05 >= 1.05/(lum+.05)) "black" else "white"
}

map_panel <- function(kind) {
  par(mar=c(3,1,3.8,1),xpd=NA,fg="#102238")
  plot(NA, xlim=c(.4,17.4),ylim=c(9.5,.5),axes=FALSE,ann=FALSE,asp=1)
  for (i in seq_len(nrow(tiles))) {
    x<-tiles$col[i]; y<-tiles$row[i]
    if(kind=="law") fill<-colors[tiles$law_level[i]] else {
      idx<-max(1,min(128,1+floor(tiles$firearm_death_rate_2024[i]/rate_max*127)))
      fill<-rate_colors[idx]
    }
    rect(x-.44,y-.44,x+.44,y+.44,col=fill,border="white",lwd=2)
    text(x,y-.11,tiles$abbr[i],col=readable(fill),font=2,cex=1.03)
    value<-if(kind=="law") paste0("L",tiles$law_level[i]) else sprintf("%.1f",tiles$firearm_death_rate_2024[i])
    text(x,y+.23,value,col=readable(fill),cex=.76)
  }
  title(main=if(kind=="law") "22 states are most lax; 13 are strictest" else "Hawaii has the lowest rate; Mississippi has the highest",
        adj=0,line=1.1,cex.main=1.38,col.main="#102238")
  mtext(if(kind=="law") "2024 law strength: every tile prints its assigned level" else
        "2024 CDC annual age-adjusted firearm deaths per 100,000",side=3,adj=0,line=.1,cex=.98,col="#42556a")
  if(kind=="law") {
    for(k in 1:5) {
      rect(.65+(k-1)*2.42,8.70,1.00+(k-1)*2.42,9.02,col=colors[k],border=NA)
      text(1.06+(k-1)*2.42,8.86,c("1 Most lax (F)","2 Lax (D)","3 Middle (C)","4 Strict (B)","5 Strictest (A)")[k],pos=4,cex=.73)
    }
    text(13.15,2.35,"MOST LAX",adj=0,font=2,cex=1.05)
    text(13.15,3.0,"22 / 50 states (44%)",adj=0,font=2,cex=1.20)
    text(13.15,3.65,"F grades become level 1",adj=0,cex=.92)
    text(13.15,5.0,"STRICTEST",adj=0,font=2,cex=1.05)
    text(13.15,5.65,"13 / 50 states (26%)",adj=0,font=2,cex=1.20)
    text(13.15,6.30,"A grades become level 5",adj=0,cex=.92)
    text(13.15,7.65,"GIFFORDS 2024 law grades",adj=0,cex=.83,col="#42556a")
  } else {
    # Numbered outlines locate the labeled extremes and the counterexample.
    for(k in seq_along(c("HI","MS","NM"))) {
      v<-tiles[tiles$abbr==c("HI","MS","NM")[k],]
      rect(v$col-.46,v$row-.46,v$col+.46,v$row+.46,border="#102238",lwd=3)
      text(v$col+.38,v$row-.61,paste0("[",k,"]"),cex=.85,font=2)
    }
    text(13.15,2.0,"[1] Hawaii: 3.7",adj=0,font=2,cex=1.25)
    text(13.15,2.7,"Lowest rate / strictest (A)",adj=0,cex=.94)
    text(13.15,4.0,"[2] Mississippi: 28.0",adj=0,font=2,cex=1.25)
    text(13.15,4.7,"Highest rate / most lax (F)",adj=0,cex=.94)
    text(13.15,6.0,"[3] New Mexico: 26.6",adj=0,font=2,cex=1.25)
    text(13.15,6.7,"Strict (B-) with high mortality",adj=0,cex=.94)
    text(13.15,7.35,"The pattern has exceptions",adj=0,cex=.92,col="#42556a")
    for(k in 0:119) rect(.68+k*.068,8.76,.68+(k+1)*.068,9.04,
                         col=rate_colors[1+floor(k/119*127)],border=NA)
    text(.68,9.20,"0",pos=4,cex=.78);text(8.65,9.20,"30",pos=4,cex=.78)
    text(9.2,8.89,"deaths / 100,000",pos=4,cex=.80,col="#42556a")
  }
  mtext("One equal-size tile per state. Schematic geography. Sources: CDC API and GIFFORDS 2024.",side=1,adj=0,cex=.78,col="#42556a",line=1.1)
}

for (kind in c("law","rate")) {
  stem<-if(kind=="law") "01_law_strength_heatmap" else "02_firearm_mortality_heatmap"
  png(file.path("figures",paste0(stem,".png")),width=2600,height=1450,res=210,bg="white")
  map_panel(kind); dev.off()
  pdf(file.path("figures",paste0(stem,".pdf")),width=12.38,height=6.90,bg="white",useDingbats=FALSE)
  map_panel(kind); dev.off()
}

# A third heat map counts states in each law category and mortality interval.
# It displays uneven group sizes directly rather than implying equal group sizes.
breaks<-c(0,8,12,16,20,30)
dat$rate_band<-cut(dat$firearm_death_rate_2024,breaks=breaks,include.lowest=TRUE,right=FALSE)
freq<-table(factor(dat$law_level,levels=1:5),dat$rate_band)
band_table <- as.data.frame(freq)
names(band_table) <- c("law_level", "mortality_band", "state_count")
band_table$group_states <- as.integer(rowSums(freq)[as.integer(band_table$law_level)])
band_table$percent_of_group <- 100 * band_table$state_count / band_table$group_states
write.csv(band_table, "data/processed/mortality_band_counts_and_shares.csv", row.names=FALSE)
draw_counts<-function() {
  par(mar=c(5,8,4,1),fg="#102238",xpd=NA)
  plot(NA,xlim=c(.5,9),ylim=c(.15,5.6),axes=FALSE,ann=FALSE,asp=1)
  cells<-rev(grDevices::hcl.colors(101,"Blues 3"))
  totals<-rowSums(freq)
  for (i in 1:5) for(j in 1:5) {
    n<-freq[i,j]; pct<-100*n/totals[i]
    fill<-cells[1+round(pct)]
    rect(j-.48,6-i-.48,j+.48,6-i+.48,col=fill,border="white",lwd=3)
    text(j,6-i+.10,n,cex=1.55,font=2,col=readable(fill))
    text(j,6-i-.22,sprintf("%.0f%%",pct),cex=.88,col=readable(fill))
  }
  axis(1,at=1:5,labels=c("0 to <8","8 to <12","12 to <16","16 to <20","20 to <30"),tick=FALSE,cex.axis=.86)
  axis(2,at=5:1,labels=paste0(c("1 Most lax (F)","2 Lax (D)","3 Middle (C)","4 Strict (B)","5 Strictest (A)"),"\n",totals," states"),las=1,tick=FALSE,cex.axis=.90)
  # Outlines and nearby descriptions make the two comparisons explicit.
  rect(3.51,4.51,5.49,5.49,border="#102238",lwd=3)
  rect(.51,.51,1.49,1.49,border="#102238",lwd=3)
  segments(5.50,5,5.95,5,lwd=2,col="#102238")
  text(6.1,5.03,"68% of most-lax states",adj=0,font=2,cex=1.07)
  text(6.1,4.54,"15 / 22 have rates of 16 or more",adj=0,cex=.89)
  segments(1,.50,1,.30,lwd=2,col="#102238")
  segments(1,.30,5.85,.30,lwd=2,col="#102238")
  segments(5.85,.30,5.85,1.05,lwd=2,col="#102238")
  segments(5.85,1.05,5.95,1.05,lwd=2,col="#102238")
  text(6.1,1.13,"54% of strictest states",adj=0,font=2,cex=1.07)
  text(6.1,.65,"7 / 13 have rates below 8",adj=0,cex=.89)
  title(main="Most-lax states cluster high; strictest states cluster low",adj=0,line=1.4,cex.main=1.22)
  mtext("Cell labels: state count and percent within each law group. Darker blue = larger share.",side=3,adj=0,line=.3,cex=.87,col="#42556a")
  mtext("2024 firearm deaths per 100,000, age-adjusted",side=1,line=2.3,adj=0,cex=.88)
  text(6.1,3.35,"Color scale: share of row",adj=0,font=2,cex=.90)
  for(k in 0:99) rect(6.1+k*.024,2.81,6.1+(k+1)*.024,3.02,col=cells[k+1],border=NA)
  text(6.1,2.57,"0%",adj=0,cex=.82);text(8.5,2.57,"100%",adj=1,cex=.82)
  text(6.1,2.0,"Unequal group sizes remain visible",adj=0,cex=.82,col="#42556a")
  mtext("Rounded percentages may not total 100%. Sources: CDC API and GIFFORDS 2024.",side=1,line=3.5,adj=0,cex=.73,col="#42556a")
}
png("figures/03_law_by_mortality_count_heatmap.png",width=2600,height=1450,res=210,bg="white")
draw_counts();dev.off()
pdf("figures/03_law_by_mortality_count_heatmap.pdf",width=12.38,height=6.90,bg="white",useDingbats=FALSE)
draw_counts();dev.off()
cat("Rendered three annotated heat maps in figures/ from",nrow(dat),"states.\n")

