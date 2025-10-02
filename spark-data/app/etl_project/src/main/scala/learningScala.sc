//------------ tìm số chẵn trong list và tính tổng
//dùng for
//val numbers = List(1, 2, 3, 4, 5, 6)
//var sum = 0
//for(a <- numbers if a % 2 == 0){
//    sum = sum + a
//}
//println(s"Tổng các số chẵn là: " + sum)
//
////dùng filter
//val numbers = List(1, 2, 3, 4, 5, 6)
//val sum = numbers.filter(_ % 2 == 0).sum
//println(s"Tổng các số chẵn là: $sum")
//
////dùng collect
//val numbers = List(1, 2, 3, 4, 5, 6)
//val sum = numbers.collect { case x if x % 2 == 0 => x }.sum
//println(s"Tổng các số chẵn là: $sum")
//
////dùng foldleft
//val numbers = List(1, 2, 3, 4, 5, 6)
//val sum = numbers.foldLeft(0)((acc, x) => if (x % 2 == 0) acc + x else acc)
//println(s"Tổng các số chẵn là: $sum")


//--------------- tìm số lớn nhất trong list
//val numbers = List(1,2,3,4,5,6,712313,8,9,99)
////dùng for
//var max_num = numbers.head
//for(a <- numbers if a > max_num) {
//  max_num = a
//}
//println(s"Số lớn nhất là: $max_num")
//
////dùng max
//val max_num = numbers.max
//println(s"Số lớn nhất là: $max_num")
//
////dùng maxBy
//
//val max_num = numbers.maxBy(x => x)
//println(s"Số lớn nhất là: $max_num")
//
////dùng reduceLeft
//val max_num = numbers.reduceLeft((a, b) => if (a > b) a else b)
//println(s"Số lớn nhất là: $max_num")
//
////dùng foldLeft
//val max_num = numbers.foldLeft(Int.MinValue)((acc, x) => if (x > acc) x else acc)
//println(s"Số lớn nhất là: $max_num")


//---------- tìm số lần xuất hiện của phần tử trong list và in ra theo dạng cặp (giá tr, số lần)
//val numbers = List(1, 2, 2, 3, 1, 4, 2)
////dùng groupBy
//val count = numbers.groupBy(identity).mapValues(_.size)
//count.foreach{
//  case (value, count) =>
//  println(s"$value xuất hiện $count lần")
//}


//------------ đảo ngược chuỗi
//val string = "scala"
////dùng reverse
//println(string.reverse)
//
////foldLeft
//val string_reverse = string.foldLeft("")((acc, a) => a + acc)
//println(string_reverse)
//
////foldRight
//val string_reverse = string.foldRight("")((c, acc) => acc + c)
//println(string_reverse)

//------------ tìm số nguyên tố

//val n = 19
//var isPrime = true
//
//if (n < 2) isPrime = false
//else {
//  for (i <- 2 to scala.math.sqrt(n).toInt if isPrime) {
//    if (n % i == 0) isPrime = false
//  }
//}
//
//println(s"$n " + (if (isPrime) "là số nguyên tố" else "không phải số nguyên tố"))
//
//
//val isPrime2 =
//  n > 1 && (2 to scala.math.sqrt(n).toInt).forall(i => n % i != 0)
//println(s"$n " + (if (isPrime2) "là số nguyên tố" else "không phải số nguyên tố"))

//------


