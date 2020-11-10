declare -a arr=("dnB0rWq2T3XNlOHWObP6exuBVjMtI3S4BdDssUi5s4iuCgO9VK2xcpndNSfWPa3d" "7hMrKo1CbbhS58I85uaZtfz2cKUFbDIXlZEIGzCqXEMu7V8QcqjYBonrU93GfH1U")

for i in "${arr[@]}"
do
   nohup python3 market_maker.py "$i" &
done
