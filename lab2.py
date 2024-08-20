import numpy as np

def rd(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                data.append(float(line.strip()))
            except ValueError:
                print(f"Ошибка: невозможно преобразовать строку '{line.strip()}' в число.")
                return None
    return np.array(data)

#Вычисление средних значений и стандартных отклонений выборок
def calculate_statistics(sample1, sample2):
    mean1 = np.mean(sample1) #среднее значение
    mean2 = np.mean(sample2) #среднее значение
    std1 = np.std(sample1, ddof=1) #ст.отклонение
    std2 = np.std(sample2, ddof=1) #ст.отклонение
    return mean1, mean2, std1, std2

#Вычисление t
def calculate_t_statistic(sample1, sample2):
    n1 = len(sample1) #размер выборки data_file1
    n2 = len(sample2) #размер выборки data_file2
    degrees_of_freedom = n1 + n2 - 2 #кол-во независимых элем.данных
    pooled_std = np.sqrt(((n1 - 1) * np.var(sample1, ddof=1) + (n2 - 1) * np.var(sample2, ddof=1)) / degrees_of_freedom) 
    #корень(((первая выборка - 1)* несмещ дисперсии первой выборки + (вторая выборка - 1)* несмещ дисперсии второй выборки)/ degrees_of_freedom)
    t_statistic = (np.mean(sample1) - np.mean(sample2)) / (pooled_std * np.sqrt(1/n1 + 1/n2))
    #(среднее значение вб1 - среднее значение вб2) / (pooled_std *(корень(1/c.з.вб1 + 1/с.з.вб2))
    return t_statistic, degrees_of_freedom

#Вычисление p-значения
def calculate_p_value(t_statistic, degrees_of_freedom):
    t_distribution = np.random.standard_t(degrees_of_freedom, size=1000000)
    p_value = (np.sum(np.abs(t_distribution) > np.abs(t_statistic)) / 1000000) * 2
    return p_value

#Оценка статистической значимости результатов
def evaluate_results(p_value, alpha=0.05):
    if p_value < alpha:
        return "Отвергаем нулевую гипотезу: средние значения различаются."
    else:
        return "Нет достаточных доказательств для отвержения нулевой гипотезы."

#Функция для критерия Фишера
def fisher_test(data1, data2, data3, data4):
    var1 = np.var(data1, ddof=1)
    var2 = np.var(data2, ddof=1)
    var3 = np.var(data3, ddof=1)
    var4 = np.var(data4, ddof=1)
    
    f_statistic = max([var1, var2, var3, var4]) / min([var1, var2, var3, var4])
    
    dfn = 3
    dfd = len(data1) + len(data2) + len(data3) + len(data4) - 4
    critical_value = 2.6
    
    if f_statistic > critical_value:
        return f_statistic, "Отвергаем нулевую гипотезу: дисперсии не равны."
    else:
        return f_statistic, "Не удалось отвергнуть нулевую гипотезу: дисперсии равны."

#поулчение данных из текстовиков
data_file1 = "var5.txt"
data_file2 = "var6.txt"
data_file3 = "var7.txt"
data_file4 = "var8.txt"
#1 часть
data1 = rd(data_file1)
data2 = rd(data_file2)
#2 часть
data3 = rd(data_file1)
data4 = rd(data_file2)
data5 = rd(data_file3)
data6 = rd(data_file4)

# Вычисление статистик и t-статистики
mean1, mean2, std1, std2 = calculate_statistics(data1, data2)
t_statistic, degrees_of_freedom = calculate_t_statistic(data1, data2)

#Вычисление p
p_value = calculate_p_value(t_statistic, degrees_of_freedom)

#Вывод результатов для t-теста
print("Значение t-статистики:", t_statistic)
print("p-значение:", p_value)
print(evaluate_results(p_value))

#Вызываем функцию для проверки гипотезы Фишера
f_statistic, result = fisher_test(data3, data4, data5, data6)

#Выводим результаты для критерия Фишера
print("F-статистика:", f_statistic)
print(result)