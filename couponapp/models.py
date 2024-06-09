from django.db import models
class Department(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return self.name

class Provost(models.Model):
    teacherId=models.IntegerField(blank=True,null=True)
    name=models.CharField(max_length=100,blank=True,null=True)
    designation=models.CharField(max_length=100,blank=True,null=True)
    mobile=models.CharField(max_length=11,blank=True,null=True)
    username=models.CharField(max_length=100,blank=True,null=True)
    password=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField(max_length=100,blank=True,null=True)
    def __str__(self):
        return str(str(self.teacherId)+" - "+str(self.name))
class Manager(models.Model):
    staffId=models.IntegerField(blank=True,null=True)
    name=models.CharField(max_length=100,blank=True,null=True)
    mobile=models.CharField(max_length=11,blank=True,null=True)
    username=models.CharField(max_length=100,blank=True,null=True)
    password=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField(max_length=100,blank=True,null=True)
    def __str__(self):
        return str(str(self.staffId)+' - '+str(self.name))
class Hall(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    provost=models.OneToOneField(Provost,on_delete=models.CASCADE)
    manager=models.OneToOneField(Manager,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name
class Shift(models.Model):
    name=models.CharField(max_length=20,blank=True,null=True)
    def __str__(self):
        return self.name
class Menu(models.Model):
    menuId=models.IntegerField(blank=True,null=True)
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE)
    menuType=models.ForeignKey(Shift,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)
    desc=models.CharField(max_length=300,blank=True,null=True)
    image=models.ImageField(upload_to='image/' ,blank=True,null=True)
    def __str__(self):
        return str(str(self.menuId)+" - "+str(self.name))
class AddOns(models.Model):
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE,blank=True,null=True)
    addOnId=models.IntegerField(blank=True,null=True)
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)
    def __str__(self):
        return str(str(self.hall.name)+" - "+str(self.addOnId)+" - "+str(self.name))
    
class Student(models.Model):
    studentId=models.IntegerField(blank=True,null=True)
    session=models.CharField(blank=True,null=True,max_length=100)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE)
    username=models.CharField(max_length=100,blank=True,null=True)
    password=models.CharField(max_length=100,blank=True,null=True)
    name=models.CharField(blank=True,null=True,max_length=100)
    email=models.EmailField(blank=True,null=True,max_length=100)
    request=models.IntegerField(default=0)
    def __str__(self):
        return str(str(self.studentId)+" - "+str(self.name))
class Feast(models.Model):
    feastId=models.IntegerField(default=0)
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE)
    date=models.DateField(null=True,blank=True)
    name=models.CharField(max_length=100,blank=True,null=True)
    price=models.IntegerField(default=0)
    desc=models.TextField(max_length=400,blank=True,null=True)
    def __str__(self):
        return str(str(self.date)+" - "+(self.name)+" - "+str(self.hall.name))
class couponMenu(models.Model):
    email=models.EmailField(blank=True,null=True)
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE,null=True)
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)
    qt=models.IntegerField(default=0)
    processed=models.IntegerField(default=0)
    def __str__(self):
        return str(str(self.email)+" - "+str(self.menu.menuId))
class couponAdd(models.Model):
    email=models.EmailField(blank=True,null=True)
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE,null=True)
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)
    addOn=models.ForeignKey(AddOns,on_delete=models.CASCADE)
    qt=models.IntegerField(default=0)
    processed=models.IntegerField(default=0)
    def __str__(self):
        return str(str(self.email)+" - "+str(self.addOn.addOnId))
class feastCoupon(models.Model):
    email=models.EmailField(blank=True,null=True)
    feast=models.ForeignKey(Feast,on_delete=models.CASCADE)
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(str(self.email)+" - "+str(self.feast.feastId))
class soldMenu(models.Model):
    date=models.DateField(blank=True,null=True)
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE,null=True)
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)
    qt=models.IntegerField(default=0)
    def __str__(self):
        return str(str(self.date)+" - "+str(self.hall.name)+" - "+str(self.menu.menuId))
class indCoupon(models.Model):
    couponId=models.IntegerField(null=True)
    date=models.DateField(blank=True,null=True)
    hall=models.ForeignKey(Hall,on_delete=models.CASCADE)
    couponMenu=models.ForeignKey(couponMenu,on_delete=models.CASCADE,null=True)
    couponAdd=models.ForeignKey(couponAdd,on_delete=models.CASCADE,null=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    def __str__(self):
        return str(str(self.student.studentId)+" - "+str(self.couponId))
