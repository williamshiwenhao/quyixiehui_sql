# 曲艺协会数据库查询脚本

为方便统计协会数据，写了一个Python脚本用来一键统计协会的演出数据。

### 依赖

Python3

mysql-connector

### 使用方法

创建config.py文件并在其中写明数据库的参数，需要参数如下

```python
host = myssql服务器所在地址
port = mysql的端口，一般都是3306
user = 用户名
passwd = 密码
database = "quyixiehui"#库名称，可能不一样
```

用户需要有select, drop, create tempory table的权限

另外如果数据库迁移，数据库版本的不一致可能会改变加密方式，需要修改main.py中的auth_plugin='mysql_native_password'内容。

如果一切正常的话直接运行main.py即可。

### 输出

Markdown格式，在执行目录下。