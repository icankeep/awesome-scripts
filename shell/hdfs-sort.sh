# sort by size
hdfs dfs -du -h {path} | sed 's/ //' | sort -rh

# sum of size
awk '
{
  if($0~/[kK]$/){
    sum+=($0+0)/(1024*1024)
  }
  if($0~/[mM]$/){
    sum+=($0+0)/(1024)
  }
  if($0~/[gG]$/){
    sum+=$0+0
  }
  if($0~/bB]$/){
    sum+=($0+0)/(1024*1024*1024)
  }
}
END{
  print sum
}
'
