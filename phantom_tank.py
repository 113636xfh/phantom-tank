#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 15:10:22 2021

@author: xfh
"""

import os 
from PIL import Image
from multiprocessing import Pool,Lock
import numpy as np
from functools import wraps
import time

def my_time(fun):
    @wraps(fun)
    def f(*args):
        begin = time.time()
        fu = fun(*args)
        end = time.time()
        print(str(fun.__name__),':spend time:', 1000*(end-begin), 'ms')
        return fu
    return f

class Img_list:
    def __init__(self, transpose_bool = False):
        self.in_imgs = self.mk_imgs('in')
        self.out_imgs = self.mk_imgs('out')
        self.transpose_bool = transpose_bool
        
    def mk_imgs(self,path):
        files = os.listdir(path)
        files = list(map(lambda x:os.path.join(path, x),files))
        files = sorted(files,key = lambda x : os.path.getatime(x))
        for file in files:
            name = file.split('/')[-1].split('.')[0]
            #Windows下前一行改为name = file.split(r'\\')[-1].split('.')[0]
            img = Image.open(file).convert('L')
            if img.size[0] < img.size[1] and self.transpose_bool:
                img = img.transpose(Image.ROTATE_90)
                print('transposed')
            yield img, name
            
    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.in_imgs), next(self.out_imgs)
            
class Mk_tank():
    def __init__(self, img_in, img_out):
        self.img_in = img_in[0]
        self.img_out = img_out[0]
        self.name = img_in[1] + '-' + img_out[1]
        
    def img_resize(self):
        #print(self.img_in)
        k_0 = self.img_out.size[0] / self.img_in.size[0]
        k_1 = self.img_out.size[1] / self.img_in.size[1]
        #print(4)
        if k_0 < 1 and k_1 < 1:
            self.img_out = self.img_out.resize(int(x / max(k_0,k_1)) for x in self.img_out.size)
        else:
            self.img_in = self.img_in.resize(int(x * min(k_0,k_1)) for x in self.img_in.size)
        #print(self.img_in.size,self.img_out.size)
            
    def set_mat(self, img_out, img_in):
        shape = max(img_in.size, img_out.size)
        mat_in = self.set_back(shape, img_in)
        mat_out = self.set_back(shape, img_out)
        return mat_in, mat_out    
            
    def set_back(self, shape, img):
        shape = np.add(shape, 1)
        mat =  np.zeros(shape)
        d_shape = np.subtract(mat.shape,img.size)
        mod = d_shape % 2
        d_shape = d_shape // 2
        mat[d_shape[0] : -d_shape[0] - mod[0], d_shape[1] : -d_shape[1] - mod[1]] = np.array(img).T
        return mat.T
    
    def mk_tank(self):
        lock = Lock()
        #print(lock)
        mat_in, mat_out = self.set_mat(self.img_out, self.img_in)
        while (mat_in + 20 > mat_out).any():
            mat_out += 10
        h = mat_out.max()
        mat_in /= h/255
        mat_out /= h/255
        a_mat = 255 - mat_out + mat_in + 1
        c_mat = mat_in * 255 / a_mat
        new_pic_mat = np.zeros(a_mat.shape + (4,))
        new_pic_mat[:,:,0:3] += c_mat[:,:,np.newaxis]
        new_pic_mat[:,:,3] = a_mat
        new_pic_img = Image.fromarray(np.uint8(new_pic_mat)).convert('RGBA')
        name = self.name
        new_pic_img.save('./new/' + name + '.png')
        lock.acquire()
        print(name,'成功生成')
        lock.release()
        
def mk(img_in, img_out):
    tank = Mk_tank(img_in, img_out)
    tank.img_resize()
    tank.mk_tank()

@my_time
def main():
    pool = Pool()
    imgs = Img_list()
    for img_in,img_out in imgs:
        #print(img_in,img_out)
        pool.apply_async(mk,(img_in, img_out))
    pool.close()
    pool.join()
    
if __name__ == '__main__':
    main()
        

