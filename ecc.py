#!/usr/bin/env python
# coding: utf-8

# ## Importing Libraries

# In[1]:


#import numpy as np
import math
import random
#import tqdm
#import matplotlib.image as Image
#import matplotlib.pyplot as plt
#from IPython.display import Markdown as md


# # Functions
# 
# ## Functions 1.1 - Modulo Inverse
# The modulo inverse of $a$ modulo $m$ is denoted as $a^{-1}$ and is defined as the integer $x$ such that
# \begin{equation}
# ax \equiv 1 \pmod{m}.
# \end{equation}

# In[2]:


def moduloInverse(a,m):
    for i in range(1,m):
        if (a*i)%m==1:                   # a*a^-1 = 1,  a^-1 = i
            return i


# ## Functions 1.2 - Lambda Generator
# 
# In order to apply point addition on elliptic curves, we have to find slope of tangent line drawn with P and Q points.To find a slope of two points, we use following equations:
# \begin{equation}
# \begin{aligned}
#     \text{if points are same} , \quad & l = \frac{3(p_1^2) + a}{2q_1} \mod p, \\
#     \text{else,} \quad & l = \frac{q_2 - q_1}{p_2 - p_1} \mod p.
# \end{aligned}
# \end{equation}
# 
# As seen, we use derivative of the elliptic curve equation while the two points to be added are same.
# 

# In[3]:


def lambdaGenerator(p1,q1,p2,q2,a,b,p):
    if(p1==p2 and q1==q2):
        l=((3*(p1**2)+a)*moduloInverse(2*q1,p))%p #derivative of the elliptic curve equation to draw line. Derivative = 3x^2 + a
    else:
        l=((q2-q1)*moduloInverse(p2-p1,p))%p  # slope's formula = (q₂ - q₁)/(p₂ - p₁). The (1 / (p₂ - p₁)) = modulo inverse of point).
    return l


# ## Functions 1.3 - Point Addition
# 
# To perform addition of two distinct point coordinate the following calculation is used. When one of the points are (0,0) the other point is the result. When the additive inverse case occurs, the function returns 0.
# The additive inverse case as follows:
#     \begin{equation}
#     \begin{aligned}
#         \text{if } (q_1 + q_2) \mod p = 0 \text{ and } p_1 = p_2, \quad & (p_3, q_3) = (0,0).
#     \end{aligned}
#     \end{equation}
# 
# The point addition is defined as follows:
#     \begin{align*}
#         &P(p_1, q_1) + Q(p_2, q_2) = R(p_3, q_3) \\ \\
#         &p_3 = \left(\frac{q_2 - q_1}{p_2 - p_1}\right)^2 - p_1 - p_2 \mod p \\ \\
#         &q_3 = \frac{q_2 - q_1}{p_2 - p_1}(p_1 - p_3) - q_1 \mod p
#     \end{align*}

# In[4]:


def pointAddition(p1,q1,p2,q2,a,b,p):
    if(p1==0 and q1==0):         #when one point is 0,0
        return p2,q2
    if(p2==0 and q2==0):         #when one point is 0,0
        return p1,q1
    if((q1+q2)%p==0 and p1==p2): #the additive inverse case  P + (−P) = Identity Element (0,0), generally defined as infinite.
        return 0,0
    l=lambdaGenerator(p1,q1,p2,q2,a,b,p)
    p3=(l**2-p1-p2)%p
    q3=(l*(p1-p3)-q1)%p
    return p3,q3


# ## Functions 1.4 Point Multiplication
# 
# Given a point $P = (x,y)$ on the curve and an integer $k$, a
# scalar multiplication on the curve is obtained as
# \begin{equation}
# kP =  \underbrace{P + P + ... + P.}_{k \text{ times}}
# \end{equation}

# In[5]:


def pointMultiplication(p1,q1,a,b,p,n):
    n = n - 1
    inip1=p1
    iniq1=q1
    while(n>0):
        if(n%2==1):
            p1,q1=pointAddition(p1,q1,inip1,iniq1,a,b,p)
            #print(p1,q1)
        inip1,iniq1=pointAddition(inip1,iniq1,inip1,iniq1,a,b,p)
        n=n//2
    return p1,q1


# In[6]:


#in my elliptic curve domain, the order of point P = (2,77) is 261.
print(pointMultiplication(2,77,195,154,283,261))
print(pointMultiplication(2,77,195,154,283,1))


# ## Functions 1.5 Is Point on Curve
# 
# This function takes point and elliptic curve. The function returns true if given point is on the curve, false otherwise.

# In[7]:


def isPointOnCurve(p1, q1, a, b, p):
    if (q1**2) % p == (p1**3 + a*p1 + b) % p:
        print(p1,",",q1," is on the curve.")
        return True
    else:
        print(p1,",",q1," is not on the curve.")
        return False


# ## Functions 1.6 Negative Of Point
# 
# This function takes a point and returns negative of this point.
# 
# ![ch4_elliptic_curve_plots_69126.png](attachment:99152033-311b-4d50-a1ff-5ad67e0d92f4.png)

# In[8]:


def negativeOfPoint(p1,q1,p):
    return p1,-q1%p 


# ## Functions 1.7 Key Generator
# 
# This function takes elliptic curve domain and returns public key and secret key.
# 
# $\textit{Input: An elliptic curve E, the point P, prime number p, prime order n that P has.}$
# <br>
# $\textit{Output: A public key pk and secret key sk.}$
# <br>
# 
# $1. \textit{choose sk }  \in_R [1, n - 1]$
# <br>
# $2. \textit{pk } \longleftarrow \textit{sk } \cdot P$
# <br>
# $3. \textbf{return} \textit{ pk, sk}$

# In[9]:


def keyGenerator(a,b,p,order,gen):
    nx=random.randint(1,order-1)
    print("The secret key is ",nx)
    px,py=pointMultiplication(gen[0],gen[1],a,b,p,nx)
    print("The public key is ",px,py)
    return (px,py), nx


# ## Functions 1.8 Encrypt
# 
# This function takes point and elliptic curve domain and a plaintext to be encrypted. It returns ciphertexts.
# 
# $\textit{Input: An elliptic curve E, the point P, prime number p, prime order n that P has, public key pk, plaintext m.}$
# <br>
# $\textit{Output: Ciphertext($C_1, C_2$).}$
# 
# $1. \textit{represent the plaintext m as a point M in } E(\mathbb{F}_p)$
# <br>
# $2. \textbf{choose } k \in_R [1, n - 1]$
# <br>
# $3. C_1 \longleftarrow k \cdot P$
# <br>
# $4. C_2 \longleftarrow M + pk \cdot k$
# <br>
# $5. \textbf{return } C_1, C_2$

# In[10]:


def encrypt(plaintext,a,b,p,order,gen,px,py, pixelToPoint,generatorLookup):
    point = pixelToPoint[plaintext]
    
    k=random.randint(1,order-1)
    #c1 = pointMultiplication(gen[0],gen[1],a,b,p,k)

    c1 = generatorLookup[k]

    p2, q2 = pointMultiplication(px,py,a,b,p,k)
    c2 = pointAddition(point[0],point[1],p2,q2,a,b,p)
    
    return c1,c2


# ## Functions 1.9 Decrypt
# 
# This function takes point and elliptic curve domain and a ciphertext to be decrypted. It returns the original plaintext.
# 
# $\textit{Input: An elliptic curve E, the point P, prime number p, prime order n that P has, private key sk, ciphertext ($C_1, C_2$).}$
# <br>
# $\textit{Output: Plaintext m.}$
# 
# 
# $1. M \longleftarrow C_2 - sk \cdot C_1$
# <br>
# $2. \textit{represent the point M as a plaintext m}$
# <br>
# $3. \textbf{return } m$
# <br>
# <br>
# $M = C_2 - sk \cdot C_1 = (M + pk \cdot k) - (sk \cdot k \cdot P) = M + (sk \cdot P \cdot k) - (sk \cdot k \cdot P) = M$

# In[11]:


def decrypt(c1,c2,p,a,b,order,nx, pointToPixel):
    p2,q2 = pointMultiplication(c1[0],c1[1],a,b,p,nx)
    p2,q2 = negativeOfPoint(p2,q2,p)

    M = pointAddition(c2[0],c2[1],p2,q2,a,b,p)

    m = pointToPixel[M]

    return m


# ## Functions 1.10 Find all points on the curve
# 
# This function takes elliptic curve and finds all points on the curve.

# In[12]:


def findPoints(a,b,p):
    points=[]
    for i in range(p):
        for j in range(p):
            if((j**2)%p==((i**3+a*i+b)%p)):
                points.append((i,j))
    return points


# ## Functions 1.11 Is prime
# 
# This function takes number n and returns true or false for the situation to be prime.

# In[13]:


def isPrime(n):
    if n==2:
        return True
    if n%2==0:
        return False
    for i in range(3,int(math.sqrt(n))+1,2):
        if n%i==0:
            return False
    return True


# ## Functions 1.12 Find order of point
# 
# This function founds order n of a point P in elliptic curve such that
# \begin{equation}
#     n \cdot P = \infty
# \end{equation}

# In[14]:


def findOrder(p1,q1,a,b,p,order):
    p2,q2=p1,q1
    for i in range(1,order):
        p2,q2=pointAddition(p2,q2,p1,q1,a,b,p)
        if(p2==0 and q2==0):
            return i+1
    return -1


# ## Functions 1.13 Prime number generator
# 
# This function randomly generates a prime number for $ \mathbb{F}_p$ in elliptic curve domain .

# In[15]:


def primeNumberGenerator():
    primeslist=[]
    for i in range(200,400):
        if isPrime(i):
            primeslist.append(i)
    p=random.choice(primeslist)
    return p


# ## Functions 1.13 Curve Generator
# 
# This function takes nothing and outputs elliptic curve randomly.
# Let $p$ be a prime number, and let $\mathbb{F}_p$ denote the field of integers modulo $p$. An elliptic curve $E$ over $\mathbb{F}_p$ is defined by an equation of the form
#     $y^2 = x^3 + ax + b,$
#     where $a, b \in \mathbb{F}_p$ satisfy $4a^3 + 27b^2 \not\equiv 0$ mod $p$.

# In[16]:


def curveGenerator():
    finalpoints=[]
    actualp=0
    actuala=0
    actualb=0
    gen=()
    while(True):
        p=primeNumberGenerator()
        a=random.randint(1,p-1)
        b=random.randint(1,p-1)
        while((4*(a**3)+27*(b**2))%p==0):
            a=random.randint(1,p-1)
            b=random.randint(1,p-1)
        points=findPoints(a,b,p)
        order=0
        for i in range(len(points)):
            if order<findOrder(points[i][0],points[i][1],a,b,p,len(points)+1):
                order=findOrder(points[i][0],points[i][1],a,b,p,len(points)+1)
                gen=points[i]
        if(order>=257):
            finalpoints=points
            actualp=p
            actuala=a
            actualb=b
            break
    return finalpoints,actualp,actuala,actualb,order,gen


# In[17]:

'''
print("Generating Curve")
finalpoints,p,a,b,order,generator = curveGenerator()
print("Curve Generated")
print("p =",p)
print("a =",a)
print("b =",b)
print("order =",order)
print("generator =",generator)


# In[18]:


isPointOnCurve(generator[0], generator[1], a, b, p)


# ## The elliptic curve
# 
# 
# $ E: y^2 = x^3 + 94x + 41$
# <br>
# <br>
# $\textbf{The curve is on } \mathbb{F}_{241}$
# <br>
# <br>
# $\textit{The generator point is } (2,113)$
# <br><br>
# $\textit{The order is } 262$

# In[19]:


y, x = np.ogrid[-90:90:100j, -20:20:100j]
plt.contour(x.ravel(), y.ravel(), pow(y, 2) - pow(x, 3) - x * a - b, [0])
plt.grid()
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.show()


# ## Reading Image as NumPy Array

# In[20]:


def imageToArray(image):
    img=Image.imread(image)
    img=img.reshape(-1,)
    return img

def arrayToImage(array,l,w,h):
    newimg=array.reshape(l,w,h)
    return newimg


img1D= imageToArray("cat.jpeg")
img3D=Image.imread("cat.jpeg")
length,width,height=img3D.shape
print("length is ",length)
print("width is ",width)
print("height is ",height)
print("Image shape is ",img3D.shape)
print("Image array in 1D is ",img1D)
print("Image shape in 1D is ",img1D.shape)


# ## Main program to perform operations.

# In[45]:


pixelToPoint={}
pointToPixel={}

for i in range (0,len(finalpoints)):
    pixelToPoint[i]=finalpoints[i]
    pointToPixel[finalpoints[i]]=i

isPrime(p)
# Assign public and secret key
publicKey, secretKey = keyGenerator(a, b, p, order, generator)

px = publicKey[0]
py = publicKey[1]
nx = secretKey



#Create a lookup table for generator point. 
generatorLookup = {}
for i in range(order):
    generator_x, generator_y = pointMultiplication(generator[0],generator[1],a,b,p,i)
    generatorLookup[i] = (generator_x,generator_y)


'''
'''
image = [1,5,67,32]
newImg = []
for i in range(4):
    pixel = image[i]
    cofactor = int(pixel / 32) + 1
    print(cofactor)

    px, py = pointMultiplication(publicKey[0], publicKey[1],a,b,p,cofactor)
    nx = (secretKey * cofactor) % order
    
    c1, c2 = encrypt(pixel,a,b,p,order,generator,px,py,pixelToPoint,generatorLookup)
    decryptedPixel = decrypt(c1,c2 ,p,a,b,order,nx, pointToPixel)
    newImg.append(decryptedPixel)

print(newImg)



# a normal image encryption

newimg1D=[]

encryptedImage = []
for i in tqdm.tqdm(range (0, img1D.shape[0])):
    pixel=img1D[i]
    cofactor = int(pixel / 32) + 1

    px, py = pointMultiplication(publicKey[0], publicKey[1],a,b,p,cofactor)
    nx = (secretKey * cofactor) % order
    
    c1, c2 = encrypt(pixel,a,b,p,order,generator,px,py,pixelToPoint,generatorLookup)
    encryptedImage.append((c1,c2))
    decryptedPixel=decrypt(c1,c2 ,p,a,b,order,nx, pointToPixel)
    newimg1D.append(decryptedPixel)



# In[44]:


print("The encrypted image is",encryptedImage[0])
print()
print()
print("The decrypted image is",newimg1D)


# In[39]:


newimg1D=np.array(newimg1D)
newimg3D=arrayToImage(newimg1D,length,width,height)
plt.imshow(newimg3D)

'''