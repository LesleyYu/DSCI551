# MongoDB

启动mongodb：`mongosh`

`use db552`

`db`

`show tables`

查询：`db.person.find()`

新增：`db.person.insertOne()`

​			`db.person.insertMany()`

![image-20240310041703945](./MongoDB_commands_pics/image-20240310041703945.png)

![Untitled](./MongoDB_commands_pics/1.png)

![image-20240310042356112](./MongoDB_commands_pics/image-20240310042356112.png)

![image-20240310043020006](./MongoDB_commands_pics/image-20240310043020006.png)

### Tips:

1. we can omit "" on keys when 查询.

2. logical operators:

   `$or`, `$and` can be top-level operator

​		`$not` cannot be top-level operator

3. Comparison operators:

   `$lt`, `$gt`, `$lte`, `$gte`, `$eq`, `$ne`, `$in`, `$all`

![image-20240310043833908](./MongoDB_commands_pics/image-20240310043833908.png)

![image-20240310043943198](./MongoDB_commands_pics/image-20240310043943198.png)

![image-20240310044219034](./MongoDB_commands_pics/image-20240310044219034.png)

`i` means case-insensitive.

含有数字：

![image-20240310051536647](./MongoDB_commands_pics/image-20240310051536647.png)

**start with** :`^` and **end with** : `$`

![image-20240310051928312](./MongoDB_commands_pics/image-20240310051928312.png)



### Projection

是否返回指定attribute：

![image-20240310052326800](./MongoDB_commands_pics/image-20240310052326800.png)

其中_id是特殊的。默认显示，可以通过 ` _id: 0` 来让它不显示。`xx: 0` 对其他attribute不适用。其他attribute可以写 `xx: 1`。就很神奇：

![image-20240310052708243](./MongoDB_commands_pics/image-20240310052708243.png)

原因：Can not mix 1 and 0 conditions (unless it is "_id")



### Matching elements in array

![image-20240310045932920](./MongoDB_commands_pics/image-20240310045932920.png)

![image-20240310050037654](./MongoDB_commands_pics/image-20240310050037654.png)

![image-20240310050141224](./MongoDB_commands_pics/image-20240310050141224.png)

### count

![image-20240310203521895](./MongoDB_commands_pics/image-20240310203521895.png)

 ### Condition on document elements of array

见ppt p26，27



### sorting:  `.sort()`

 1 for ascending; -1 descending

![image-20240310203841080](./MongoDB_commands_pics/image-20240310203841080.png)



### limit and skip

就等于xml里面的limit和offset

![image-20240310205012197](./MongoDB_commands_pics/image-20240310205012197.png)



### distinct

![image-20240310205214084](./MongoDB_commands_pics/image-20240310205214084.png)

以上等效于sql：`select distinct age from Person where age > 28`

![image-20240310210208311](./MongoDB_commands_pics/image-20240310210208311.png)

注意：不能和find一起用：

![image-20240310210727536](./MongoDB_commands_pics/image-20240310210727536.png)



### Renaming

`{newName: '$oldName'}`

![image-20240310211617970](./MongoDB_commands_pics/image-20240310211617970.png)







### Writing Javascript in Mongo Shell

![image-20240310212236888](./MongoDB_commands_pics/image-20240310212236888.png)

Using javascript cursor in MongoDB:

![image-20240310212706940](./MongoDB_commands_pics/image-20240310212706940.png)

Using `forEach` function in MongoDB:

![image-20240310212902344](./MongoDB_commands_pics/image-20240310212902344.png)



### Update

`updateOne`

![image-20240310214121353](./MongoDB_commands_pics/image-20240310214121353.png)

`updateMany`

![image-20240310214546142](./MongoDB_commands_pics/image-20240310214546142.png)

##### set and unset

unset就是把这个属性去掉，参数可以填任何东西。反正它也没了。标准就是填null。

![image-20240310214800534](./MongoDB_commands_pics/image-20240310214800534.png)



### _upsert_ (update if exists; otherwise insert.)

如果没有指定的复合要求的attribute，update会失败。如下图，没有_id=6。所有返回值结果都是0。

![image-20240310220201584](./MongoDB_commands_pics/image-20240310220201584.png)

啊？为什么不行？？？

![image-20240310220506739](./MongoDB_commands_pics/image-20240310220506739.png)



### delete

![image-20240310221314138](./MongoDB_commands_pics/image-20240310221314138.png)



### Remove documents, collection/table

`db.person.remove({})`   This will remove documents/records of _person_.

`db.person.remove({ _some_condition_here_ })`

`db.person.drop()     This will remove the person collection/table.



### dot operation:  Sub-strings

![image-20240310221925279](./MongoDB_commands_pics/image-20240310221925279.png)



### Aggregation 
The aggregate method in MongoDB is used for performing data aggregation operations, which involve *grouping*, *transforming*, and analyzing data from one or *more* collections. 

##### sum

![image-20240310223243255](./MongoDB_commands_pics/image-20240310223243255.png)

In sql: `select category, sum(qty) from product group by category`

##### count

![image-20240310223605209](./MongoDB_commands_pics/image-20240310223605209.png)

In sql: `select category, count(*) from product group by category`

##### aggregation with _having_

use _$match_ keyword.

![image-20240310224830218](./MongoDB_commands_pics/image-20240310224830218.png)

##### aggregation on more than one field

![image-20240310230037826](./MongoDB_commands_pics/image-20240310230037826.png)

##### aggregation pipeline

![image-20240310230627485](./MongoDB_commands_pics/image-20240310230627485.png)

##### Projection in aggregate

```txt
db.product.aggregate(
  {$group:
    {_id: null, max: {$max: "$qty"} }
  }
)

output:
{ "_id" : null, "max" : 45 }
```

Remove _id from result:

```
db.product.aggregate(
    {$group:
      {_id: null, max: {$max:"$qty"} }
    }, 
    {$project: {_id: 0} }
)

output:
{ "max" : 45 }
```


### $lookup for joining two collections

```
db.person.aggregate(
    {$lookup: {
       from: 'department', 
       localField: 'deptID', 
       foreignField: "_id", 
       as: 'res'
       }
    }, 
    {$match: 
      {name: {$ne: null}}
    }, 
    {$project: 
      {name: 1, 'res.name': 1, _id: 0}
    }
)
```

### $unwind

db.person.aggregate(
  {$unwind: '$scores'}
)