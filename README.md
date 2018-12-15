# homeassistan-component-ezviz
homeassistant component for ezviz(ys7.com) camera

这个组件支持萤石云摄像头，主要支持能捕获图像，能设置镜头遮蔽开关

##安装方法
下载custom_components文件夹中的代码，保存在<homeassistant配置目录>/custom_components/目录中，若custom_components目录不存在则自行创建。

**homeassistant配置目录**
- **Windows用户**: %APPDATA%\.homeassistant
- **Linux-based用户**: 可以通过执行locate .homeassistant/configuration.yaml命令，查找到的.homeassistant文件夹就是配置目录。
- **群晖Docker用户**: 进入Docker - 映像 - homeassistant - 高级设置 - 卷, /config对应的路径就是配置目录

##HA中配置
```yaml
# configuration.yaml
ezviz:
  DeviceName: "mycamera" #摄像头名称
  DeviceId: "xxxxxxxx" #设备序列号
  AppKey: "xxxxxxxx" #我的应用的AppKey，需要先新建应用
  Secret: "xxxxxxxx" #我的应用的Secret，需要先新建应用
```

##配置获取地址
- [获取设备序列号: https://open.ys7.com/console/device.html](https://open.ys7.com/console/device.html)
- [获取应用的AppKey和Secret: https://open.ys7.com/console/application.html](https://open.ys7.com/console/application.html)

**附**
需要支持更多功能，可以提issue，陆续补充
最后推荐组件 https://github.com/haoctopus/molobot 组件，可以不需要公网ip的情况下支持天猫精灵控制
