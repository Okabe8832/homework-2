'''

老师好！这是本节课的分支界定题目的python演示，我知晓其中所有语句的原理，代码初步设计过程参考了Ai 。：）

以下是代码的一些说明：

    Cv（当前累计价值）
	cw（当前累计重量）
	Ub（上界值）
	best（当前已知最优解）


	list_weight（物品的重量数据列表）
	list_value（物品的价值数据列表）
	list_value_weight（物品的价值/重量数据列表）
	W（背包的总负重上限）
	ratio（即v / w值）
	list_items_final（按照ratio由大到小排列的物件列表）
	class Item （物件类型，包含w,v,ratio三个方变量。对象名称为item）
	class Node（节点类型，包含level，cw,cv,ub=0三个变量和一个ub初始值。对象名称为node）
	root（初始节点，root = Node(-1, 0, 0)）
	expand函数（生成器函数，投入node后yield两个child，对应放入背包或不放入背包）
	bound函数（对node节点的ub值进行计算）
	branch_bound函数（含有一个有效节点列表，调用expand和bound，从root开始进行分支并修剪，对best更新，且传入新的有效节点形成循环）

'''




class Item:
    def __init__(self,id,w,v):
        self.w = w
        self.v = v
        self.ratio = v / w
##设置了类
list_items=[1,2,3,4]
list_weight=[4,7,5,3]
list_value=[40,42,25,12]
#list_value_weight=list(map(lambda x,y:x/y,list_value,list_weight))

list_items_final=[]
for id,w,v in zip(list_items,list_weight,list_value):
    list_items_final.append(Item(id,w,v))
##使用zip把物品参数打包，放入物件对象后，将诸物件对象放入物件列表

list_items_final.sort(key=lambda x:x.ratio,reverse=True)
##对列表对象按照价值/重量比由大到小排列



class Node:
    def __init__(self, level, cw, cv,ub=0):
        #设定了Node节点类型，它的对象是node，初始节点使用root = Node(-1, 0, 0)的方式表现。由于大量使用三个参数的node
        self.level = level
        self.cw = cw
        self.cv = cv
        self.ub = ub


W = 10
#负重上限

##########生成器函数，用于yield两个child，对应放入背包或不放入背包的情况
def expand(node):
    next_level = node.level + 1
    if next_level >= len(list_items_final):
        return

    item = list_items_final[next_level]

    put_in_bag = Node(next_level, node.cw + item.w, node.cv + item.v)
    yield put_in_bag

    not_put_in_bag = Node(next_level, node.cw, node.cv)
    yield not_put_in_bag


##对节点ub值进行计算的函数
def bound(node):
    if node.cw >= W:
        return 0

    profit = node.cv
    weight = node.cw
    #设置两个参数表示本节点已累积的价值和重量

    i = node.level + 1
    #进入本节点的下一层

    while i < len(list_items_final) and weight + list_items_final[i].w <= W:
        #while循环中，从下一层的物件开始放入背包直到放完物件或背包到达重量上限
        weight += list_items_final[i].w
        profit += list_items_final[i].v
        #在节点累积的基础上不断累积每次新增的重量和价值
        i += 1

    if i < len(list_items_final):
        #while循环结束后，如果仍然有物件没有放入背包
        profit += (W - weight) * list_items_final[i].v / list_items_final[i].w
        #获得了剩余背包容量（若有）和下一个未能放入的物件的V/M比率。计算了本节点的ub值。
    return profit
#使用profit作为ub计算的变量名，等待绑定





def branch_and_bound():
    root = Node(-1, 0, 0)
    root.ub = bound(root)
    #绑定了初始节点的ub

    best = 0
    waiting_nodes = [root]
    #用于存储有效节点的列表，目前已存入初始节点了

    while waiting_nodes:
        node = waiting_nodes.pop()
        #取出列表最新的有效节点

        # 如果这个节点ub都小于等于 best，剪枝
        if node.ub <= best:
            continue

        for child in expand(node):
        #调用生成器函数expand，投入目前节点。目前节点被生成器函数生成了两个预选的潜在节点（意味着物件放入背包或不放入背包）

            if child.cw > W:
                continue

            # 更新当前最优值
            if child.cv > best:
                best = child.cv

            # 计算结果上界
            child.ub = bound(child)

            # 如果结果超过 best，加入有效节点列表成为一个有效节点
        ##如果两个child判定都通过，那么会出现两个node放入有效节点列表
            if child.ub > best:
                waiting_nodes.append(child)

    return best
#返回本次更新的best值，这是对child检定后更新的best值

answer = branch_and_bound()
print("最优值 =", answer)