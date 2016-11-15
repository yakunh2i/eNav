BEGIN {
step=0;
uri="http://dev.h2i.sg/ncWMS/wms?request=GetUTFGrid&digits=2&crs=CRS:84";
FS=",";
}

{ 
    if (step==0) {
        step++;
    }
    else {
        if (step==1) { #line 1
            west=$1;south=$2;east=$3;north=$4;tileSize=$5;bdate=$6;edate=$7;
            xsize=int(0.5+(east-west)/tileSize); # Unfortunately awk has only trunc, not round
            ysize=int(0.5+(north-south)/tileSize);
            step++;
        } 
        else {
            if (step==2) {
                nreq=$1;
                step++;
            }
            else {
                if (step==3) {
                    nm[nreq]=$1;grid[nreq]=$2;layers[nreq]=$3;
                    for(i=4;i<=NF;i++) {
                        layers[nreq]=sprintf("%s,%s",layers[nreq],$i);
                    }
                    nreq--;
                    if (nreq==0) {
                        step++;
                    }
                }
                else {
                    for(i=1;i<=NF;i++) {
                        tile=$i;
                        dx=int(tile/xsize);dy=(tile % ysize);
                        for(j in nm) {
                            printf("curl \"%s&time=%sT00:00:00Z/%sT23:30:00Z&layers=%s&size=%d&bbox=%s,%s,%s,%s\" -o %s_%s.json\n",uri,bdate,edate,layers[j],grid[j],west+dx*tileSize,north-(dy+1)*tileSize,west+(dx+1)*tileSize,north-dy*tileSize,nm[j],tile);
                        }
                    }
                }
            }
        }
    }
}
    
