#将需要的代码复制并cd到severless文件夹
echo "开始拷贝必要文件"
sudo cp login.py ./serverless
sudo cp main.py ./serverless
sudo cp notify.py ./serverless
sudo cp requirements.txt ./serverless
sudo cp config.json ./serverless
cd ./serverless

#删除lxml默认模块版本
echo "开始安装lxml"
sed -ie '/lxml==4.6.2/d' ./requirements.txt
#解压lxml
sudo unzip lxml.zip

#安装云函数需要的依赖库到severless文件夹
echo "开始安装所需模块"
sudo -H pip install --upgrade setuptools >/dev/null
sudo -H pip install -r ./requirements.txt -t ./

#部署至腾讯云函数
if [ -z "$TENCENT_SECRET_ID" ] || [ -z "$TENCENT_SECRET_KEY" ]; then
  echo "部署至腾讯云需要填写TENCENT_SECRET_ID和TENCENT_SECRET_KEY两个secrets，跳过部署"
else
  #腾讯云函数貌似只有 /tmp 目录能够临时存取文件
  sed -i "s/.\/log.txt/..\/..\/tmp\/log.txt/g" ./login.py
  sed -i "s/.\/log.txt/..\/..\/tmp\/log.txt/g" ./notify.py
  sed -i "s/.\/log.txt/..\/..\/tmp\/log.txt/g" ./main.py
  echo "开始安装腾讯ServerlessFramework"
  sudo npm install -g serverless
  echo "开始部署至腾讯云函数"
  sls deploy --debug
  exit 0
fi