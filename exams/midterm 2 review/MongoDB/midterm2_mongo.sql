age > 25
group by gender
min(weight)


db.person.aggregate([
  {
    $match: {
      age: { $gt: 25 }
    }
  },
  { $group: {
    _id: "$gender", val: {$min: "$weight"}
  } },
  {
    $match: {
      val: {$gt: 120}
    }
  },
  { $limit: 2 },
  { $sort: {val: -1} }
])

select gender, min(weight) as val from person
group by gender
having val > 120 
where age > 25
sort by val desc 
limit 2;


db.product.aggregate([
  {
    $group: {
      _id: "$category",
      total: { $sum: "$qty" }
    }
  },
  {
    $match: {
      total: { $qt: 50 }
    }
  }
])