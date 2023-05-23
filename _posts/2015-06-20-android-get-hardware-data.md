---
layout: single
title: 如何获取 Android 设备的CPU核数、时钟频率以及内存大小
date: 2015-06-20
categories: Android
---

因项目需要，分析了一下 Facebook 的开源项目 - [Device Year Class](https://github.com/facebook/device-year-class)。

**Device Year Class** 的主要功能是根据 *CPU核数*、*时钟频率* 以及 *内存大小* 对设备进行分级。代码很简单，只包含两个类:

* `DeviceInfo` -> 获取设备参数，
* `YearClass` -> 根据参数进行分级。

下表是 Facebook 公司提供的[分级标准](https://github.com/facebook/device-year-class/blob/master/README.md)，其中 `Year` 栏表示分级结果。

|Year|	Cores|	Clock |	RAM  |
|---:|------:|-------:|-----:|
|2008|	1    |	528MHz|	192MB|
|2009|	n/a  |	600MHz|	290MB|
|2010|	n/a  |	1.0GHz|	512MB|
|2011|	2    |	1.2GHz|	  1GB|
|2012|	4    |	1.5GHz|	1.5GB|
|2013|	n/a  |	2.0GHz|	  2GB|
|2014|	n/a  |   >2GHz|	 >2GB|

关于输出年份的计算方法可以参考[源码](https://github.com/facebook/device-year-class)，本文只把一些比较常用的功能抽取出来做一个简要介绍。


获取 CPU 核数
---

我们都知道，Linux 中的设备都是以文件的形式存在，CPU 也不例外，因此 CPU 的文件个数就等价与**核数**。

Android 的 CPU 设备文件位于 `/sys/devices/system/cpu/` 目录，文件名的的格式为 `cpu\d+`。

<pre>
root@generic_x86_64:/sys/devices/system/cpu # ls
<b>cpu0</b>
cpufreq
cpuidle
kernel_max
modalias
offline
online
possible
power
present
uevent
</pre>

统计一下文件个数便可以获得 CPU 核数。

```java
public static int getNumberOfCPUCores() {
  if (Build.VERSION.SDK_INT <= Build.VERSION_CODES.GINGERBREAD_MR1) {
    // Gingerbread doesn't support giving a single application access to both cores, but a
    // handful of devices (Atrix 4G and Droid X2 for example) were released with a dual-core
    // chipset and Gingerbread; that can let an app in the background run without impacting
    // the foreground application. But for our purposes, it makes them single core.
    return 1;
  }
  int cores;
  try {
    cores = new File("/sys/devices/system/cpu/").listFiles(CPU_FILTER).length;
  } catch (SecurityException e) {
    cores = DEVICEINFO_UNKNOWN;
  } catch (NullPointerException e) {
    cores = DEVICEINFO_UNKNOWN;
  }
  return cores;
}

private static final FileFilter CPU_FILTER = new FileFilter() {
  @Override
  public boolean accept(File pathname) {
    String path = pathname.getName();
    //regex is slow, so checking char by char.
    if (path.startsWith("cpu")) {
      for (int i = 3; i < path.length(); i++) {
        if (path.charAt(i) < '0' || path.charAt(i) > '9') {
          return false;
        }
      }
      return true;
    }
    return false;
  }
};
```

获取时钟频率
---

获取**时钟频率**需要读取系统文件 - `/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq` 或者 `/proc/cpuinfo`。

我的 Android 模拟器中并没有 `cpuinfo_max_freq` 文件，因此只能读取 `/proc/cpuinfo`。

`/proc/cpuinfo` 包含了很多 cpu 数据。

<pre>
processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 70
model name	: Intel(R) Core(TM) i7-4770HQ CPU @ 2.20GHz
stepping	: 1
cpu MHz		: 0.000
cache size	: 1024 KB
fdiv_bug	: no
hlt_bug		: no
f00f_bug	: no
coma_bug	: no
fpu		: yes
fpu_exception	: yes
cpuid level	: 4
wp		: yes
</pre>

代码如下：

```java
public static int getCPUMaxFreqKHz() {
  int maxFreq = DEVICEINFO_UNKNOWN;
  try {
    for (int i = 0; i < getNumberOfCPUCores(); i++) {
      String filename =
          "/sys/devices/system/cpu/cpu" + i + "/cpufreq/cpuinfo_max_freq";
      File cpuInfoMaxFreqFile = new File(filename);
      if (cpuInfoMaxFreqFile.exists()) {
        byte[] buffer = new byte[128];
        FileInputStream stream = new FileInputStream(cpuInfoMaxFreqFile);
        try {
          stream.read(buffer);
          int endIndex = 0;
          //Trim the first number out of the byte buffer.
          while (buffer[endIndex] >= '0' && buffer[endIndex] <= '9'
              && endIndex < buffer.length) endIndex++;
          String str = new String(buffer, 0, endIndex);
          Integer freqBound = Integer.parseInt(str);
          if (freqBound > maxFreq) maxFreq = freqBound;
        } catch (NumberFormatException e) {
          //Fall through and use /proc/cpuinfo.
        } finally {
          stream.close();
        }
      }
    }
    if (maxFreq == DEVICEINFO_UNKNOWN) {
      FileInputStream stream = new FileInputStream("/proc/cpuinfo");
      try {
        int freqBound = parseFileForValue("cpu MHz", stream);
        freqBound *= 1000; //MHz -> kHz
        if (freqBound > maxFreq) maxFreq = freqBound;
      } finally {
        stream.close();
      }
    }
  } catch (IOException e) {
    maxFreq = DEVICEINFO_UNKNOWN; //Fall through and return unknown.
  }
  return maxFreq;
}
```

获取内存大小
---

如果 SDK 版本大于等于 `JELLY_BEAN` ，可以通过 `ActivityManager` 来获取内从大小。

```java
ActivityManager.MemoryInfo memInfo = new ActivityManager.MemoryInfo();
ActivityManager am = (ActivityManager) c.getSystemService(Context.ACTIVITY_SERVICE);
am.getMemoryInfo(memInfo);
```

如果版本低于 `JELLY_BEAN` ，则只能读取系统文件了。

```java
FileInputStream stream = new FileInputStream("/proc/meminfo");
totalMem = parseFileForValue("MemTotal", stream);
```

完整代码如下：

```java
@TargetApi(Build.VERSION_CODES.JELLY_BEAN)
public static long getTotalMemory(Context c) {
  // memInfo.totalMem not supported in pre-Jelly Bean APIs.
  if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN) {
    ActivityManager.MemoryInfo memInfo = new ActivityManager.MemoryInfo();
    ActivityManager am = (ActivityManager) c.getSystemService(Context.ACTIVITY_SERVICE);
    am.getMemoryInfo(memInfo);
    if (memInfo != null) {
      return memInfo.totalMem;
    } else {
      return DEVICEINFO_UNKNOWN;
    }
  } else {
    long totalMem = DEVICEINFO_UNKNOWN;
    try {
      FileInputStream stream = new FileInputStream("/proc/meminfo");
      try {
        totalMem = parseFileForValue("MemTotal", stream);
        totalMem *= 1024;
      } finally {
        stream.close();
      }
    } catch (IOException e) {
    }
    return totalMem;
  }
}
```
