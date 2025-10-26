# 1Q.How to unpack the dictionary using while loop?

#Program;

std = {"name": "Vishnu", "age": 22, "city": "Hyderabad"}
std_list=list(std.items())
print(std_list)
count=0
while count<len(std):
    key,value=std_list[count]
    print(f"key:{key}  value:{value}")
    count+=1

# 2Q..Write a python program to print each character of all the names  present in a list one by one?

#Program:

v=[“Vishnu” , “Akash”]
for   name in v: 
  for ch in name:
    print(ch)

#3Q.Sorting the List using bubble sort?
#Program:

lst=[5,3,1,4,2]
for i in range(len(lst)):
  for j in range(len(lst)) -1):
   if lst[j]>lst[j+1]:
       lst[j],lst[j+1]=lst[j+1], lst[j]
print(“Sorted list:”,n)        #Output: Sorted list: [1,2,3,4,5]

