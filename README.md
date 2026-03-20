# Ground Routing Prefix Compression (IPv4/IPv6)

This project provides a set of tools for **ground routing prefix compression**. It converts ground prefixes (IPv4/IPv6) into **intervals** and aggregates them to reduce routing table size and lookup overhead, enabling the use of ground routing information for Satellite forwarding.

## What’s Included

- **Route compression**: supports IPv4 and IPv6
- **Incremental updates**: supports maintaining compressed results through updates
- **Interval lookup**: provides fast interval-FIB lookup and verification utilities
- **Dataset**: real-world routing prefix data  
  - IPv4: 2013–2025  
  - IPv6: 2020–2025  

More data and updates will be continuously.

## Project Structure

- `lib/`: shared utilities and common functions
- `zip/`: compression implementation  
  - `compress_IPv4.py`: main IPv4 compression pipeline  
  - `compress_IPv6.py`: main IPv6 compression pipeline  
- `update/`: incremental update module (including functions used during updates)
- `verify/`: interval lookup and result verification  
  - `verify_result.py`: verifies whether the prefix “distance” before/after compression stays within a given threshold using the interval lookup algorithm
- `data/`: datasets and intermediate artifacts  
  - real prefix data: IPv4 (2013–2025), IPv6 (2020–2025)  
  - Obtaining real prefix data and preprocessing methods
  - intermediate files generated during compression





---

# 地面路由前缀压缩（IPv4/IPv6）

本项目是一套地面路由前缀压缩程序：将地面前缀（IPv4/IPv6）转换为区间并进行聚合，以降低路由规模与查询开销，实现地面路由上“天”的目标。

## 开源内容

- **路由压缩**：支持 IPv4 与 IPv6
- **增量更新**：支持对压缩结果进行更新维护
- **区间查询**：提供区间 FIB 的快速查询与验证工具
- **数据集**：真实路由前缀数据  
  - IPv4：2013–2025  
  - IPv6：2020–2025  

后续将持续整理与更新。

## 项目结构

- `lib/`：全局通用函数与工具
- `zip/`：压缩相关实现  
  - `compress_IPv4.py`：IPv4 压缩主流程  
  - `compress_IPv6.py`：IPv6 压缩主流程  
- `update/`：增量更新模块（包含更新过程中使用的函数）
- `verify/`：区间查询与结果验证  
  - `verify_result.py`：使用区间查询算法验证压缩前后前缀“距离”是否满足设定阈值  
- `data/`：数据与中间产物  
  - 真实前缀数据：IPv4（2013–2025）、IPv6（2020–2025）
  - 获取真实前缀数据及预处理方法
  - 压缩过程中生成的中间数据文件
