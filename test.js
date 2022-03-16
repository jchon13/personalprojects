arr = []
results = []
for(i=0;i<200;i++)
{
    arr.push(i);
}

console.log(arr)

for(j=0;j<arr.length;j++){
    results.push((14+441*arr[j])/119);
}

console.log(results)