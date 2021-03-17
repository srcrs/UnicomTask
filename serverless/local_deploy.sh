#将需要的代码复制并cd到severless文件夹
echo "开始拷贝必要文件"
cp login.py ./serverless
cp main.py ./serverless
cp notify.py ./serverless
cp requirements.txt ./serverless
cp config.json ./serverless
cd ./serverless

#删除lxml默认模块版本，使用自定义模块
echo "开始安装所需模块"
sed -i '/lxml==4.6.2/d' ./requirements.txt
#解压lxml
unzip lxml.zip

#安装云函数需要的依赖库到severless文件夹
echo "开始安装所需模块"
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./requirements.txt -t ./

#部署至腾讯云函数
#腾讯云函数貌似只有 /tmp 目录能够临时存取文件
sed -i "s/.\/log.txt/..\/..\/tmp\/log.txt/g" ./login.py
sed -i "s/.\/log.txt/..\/..\/tmp\/log.txt/g" ./notify.py
sed -i "s/.\/log.txt/..\/..\/tmp\/log.txt/g" ./main.py
echo "开始安装腾讯ServerlessFramework"
npm install -g serverless --registry=https://registry.npm.taobao.org
echo "开始部署至腾讯云函数"
sls deploy --debug

#清空文件复制的文件
echo "清空所拷贝的代码"
rm -f ./login.py
rm -f ./main.py
rm -f ./notify.py
rm -f ./requirements.txt
rm -f ./config.json
exit 0