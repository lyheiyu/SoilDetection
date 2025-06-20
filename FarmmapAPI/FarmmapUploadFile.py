# import os
# import requests
# import time
# from typing import Optional
#
#
# class FarmMapsUploader:
#     def __init__(self, token: str):
#         self.token = token
#         self.base_url = "https://farmmaps.eu/api/v1/file"
#         self.chunk_size = 1048576  # 1MB
#
#     def upload_file(self, file_path: str, parent_code: str, progress_callback: Optional[callable] = None) -> dict:
#         """
#         Upload a file to FarmMaps API with progress tracking and error handling
#
#         Args:
#             file_path: Path to the file to upload
#             parent_code: Parent folder code
#             progress_callback: Optional callback function for progress updates
#
#         Returns:
#             dict: Registration response information
#         """
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"File not found: {file_path}")
#
#         file_size = os.path.getsize(file_path)
#         file_name = os.path.basename(file_path)
#
#         print(f"Uploading {file_name} ({self._format_size(file_size)})")
#
#         # Register file
#         register_info = self._register_file(parent_code, file_name, file_size)
#
#         # Upload chunks
#         self._upload_chunks(file_path, register_info, progress_callback)
#
#         print("✅ File upload completed successfully!")
#         return register_info
#
#     def _register_file(self, parent_code: str, file_name: str, file_size: int) -> dict:
#         """Register file for upload"""
#         payload = {
#             "parentCode": parent_code,
#             "name": file_name,
#             "size": file_size
#         }
#
#         # Add chunk size for large files
#         if file_size > 2 * 1024 * 1024:
#             payload["chunkSize"] = self.chunk_size
#
#         headers = {
#             "Authorization": f"Bearer {self.token}",
#             "Content-Type": "application/json"
#         }
#
#         try:
#             response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
#             response.raise_for_status()
#             register_info = response.json()
#
#             print(f"📝 File registered: {register_info['chunks']} chunk(s)")
#             return register_info
#
#         except requests.exceptions.RequestException as e:
#             raise Exception(f"Failed to register file: {e}")
#
#     def _upload_chunks(self, file_path: str, register_info: dict, progress_callback: Optional[callable] = None):
#         """Upload file chunks with retry logic"""
#         total_chunks = register_info['chunks']
#         chunk_size = register_info['chunkSize']
#         file_code = register_info['code']
#
#         upload_headers = {
#             "Authorization": f"Bearer {self.token}",
#             "Content-Type": "application/octet-stream"
#         }
#
#         with open(file_path, 'rb') as f:
#             for chunk_number in range(1, total_chunks + 1):
#                 chunk_data = f.read(chunk_size)
#
#                 if not chunk_data:
#                     break
#
#                 # Retry logic for failed chunks
#                 success = False
#                 max_retries = 3
#
#                 for attempt in range(max_retries):
#                     try:
#                         upload_url = f"{self.base_url}/{file_code}/{chunk_number}"
#                         response = requests.post(
#                             upload_url,
#                             headers=upload_headers,
#                             data=chunk_data,
#                             timeout=60
#                         )
#                         response.raise_for_status()
#                         success = True
#                         break
#
#                     except requests.exceptions.RequestException as e:
#                         if attempt < max_retries - 1:
#                             print(f"⚠️  Chunk {chunk_number} failed (attempt {attempt + 1}), retrying...")
#                             time.sleep(2 ** attempt)  # Exponential backoff
#                         else:
#                             raise Exception(f"Failed to upload chunk {chunk_number} after {max_retries} attempts: {e}")
#
#                 if success:
#                     progress = (chunk_number / total_chunks) * 100
#                     print(f"📤 Uploaded chunk {chunk_number}/{total_chunks} ({progress:.1f}%)")
#
#                     if progress_callback:
#                         progress_callback(chunk_number, total_chunks, progress)
#
#     @staticmethod
#     def _format_size(size_bytes: int) -> str:
#         """Format file size in human readable format"""
#         for unit in ['B', 'KB', 'MB', 'GB']:
#             if size_bytes < 1024.0:
#                 return f"{size_bytes:.1f} {unit}"
#             size_bytes /= 1024.0
#         return f"{size_bytes:.1f} TB"
#
#
# # Usage example
# def main():
#     # Configuration
#     # token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkNERkM3M0I0NzY0Q0M5RTYxQTVDRjg3OEM5MDlFRUU0ODFFODk5MzFSUzI1NiIsIng1dCI6InpmeHp0SFpNeWVZYVhQaDR5UW51NUlIb21URSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZhcm1tYXBzLmV1IiwibmJmIjoxNzUwMDc3ODg5LCJpYXQiOjE3NTAwNzc4ODksImV4cCI6MTc1MDA4MTQ4OSwiYXVkIjoiYXBpIiwic2NvcGUiOlsiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiZmFybW1hcHNfc3dhZ2dlciIsInN1YiI6ImI1MmRhMDhhOGE5YzRjNzlhYWVlMWU4ZDc2NTg3MTUwIiwiYXV0aF90aW1lIjoxNTAwNzc4NzYsImlkcCI6ImxvY2FsIiwic2lkIjoiMDREQkNBRkIxQkNCRENGMDE0NkZBNDc4MzU2M0VEREEiLCJhenAiOiJmYXJtbWFwc19zd2FnZ2VyIiwianRpIjoiNzhEODkyNUFFODcyOUI1QjYwM0ZEOTU1MjhDNUVEREQifQ.ssZmWUvinMKHWyBkWcoiaBpzyEAlSSOH2POErUeXKyREHPM9jq0OeFTApg4JyUXJ_fOIBC7dWnkQzvLsxVs9xb79tO648yVKL-q8-TRCMqzBXfBPU_HImnNY36-TrOErS2tYUwKHrsWPz4iTt2XalMq-Ep-JkFnQKlq6i5MWHfr82xh8kQUvOJzBrp523QXsjJQCDYBbRGvIvonupSvlXCaauOgTw6ElFwyCSRWFJpA47oc-JNbg-SYnsIgP4Op2ryaTKCRKYUH27bG6mUiLIncREsVTcfdMmGeCchGoYU1kLVOvHebAKW56MGJmmMD_rbH_V-x2cJ93L2Fys9NTdRmYCThuPIzt1Y_hznNxYQtaGCA0ZLvUt6u7krLMZvYg139-Uyp5cr_LvuLieSpaEpkFLJDpCXx_SMFXaC2YVBW_bmZVRLubW0-v_0KYOHHUOWHmO1VajTQz_-L7ZIMsqdFsZamjaaRKxbU3Y-qH2xSsZ0InrBjjDddeOLs1SsOBf2FWax7z8bj3hPON_ze4U10kNxrv6fX-AT_HpfrpIG672ngyGOussYDwSSvsFd35vBfO9DwTkmHCjhGbkrcPOPRkjtRyTCkkl1p_9DR5-FBIvWijhNxbn3KTyIobhaXM_xwOdGho-95MheIjcME6H6OF3fqYUkikUFmY-VD4xio'
#     token='eyJhbGciOiJSUzI1NiIsImtpZCI6IkNERkM3M0I0NzY0Q0M5RTYxQTVDRjg3OEM5MDlFRUU0ODFFODk5MzFSUzI1NiIsIng1dCI6InpmeHp0SFpNeWVZYVhQaDR5UW51NUlIb21URSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZhcm1tYXBzLmV1IiwibmJmIjoxNzUwMTU0NjIwLCJpYXQiOjE3NTAxNTQ2MjAsImV4cCI6MTc1MDE1ODIyMCwiYXVkIjoiYXBpIiwic2NvcGUiOlsiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiZmFybW1hcHNfc3dhZ2dlciIsInN1YiI6ImI1MmRhMDhhOGE5YzRjNzlhYWVlMWU4ZDc2NTg3MTUwIiwiYXV0aF90aW1lIjoxNzQ5NjQ5MDk0LCJpZHAiOiJsb2NhbCIsInNpZCI6IkVGQ0IxMkQyNjU3RTc2NjQ4QTU3QjBFRUZDRDNFN0RGIiwiYXpwIjoiZmFybW1hcHNfc3dhZ2dlciIsImp0aSI6IkY0MjU3NEQ1RjhGMEI5QTE4NUQxNTcyNjhGODk0RTVGIn0.e0txWsdsCI8_17A-ek4w0IhY2Jgyiq4AItXGhDchVpxPHvJb9pCgfB09QjHmmcZp4cusYd8XFlS1lLNCPRntLL6Hcg0mPddFrJAj8uzhjf47t0vEqmXgWfpEc1-tQqJvnpWHyQ6Xp_G2r_RSHuBsRNpkvjbuR0K-UR5Vb7B_LbmQGVSwPNYdIJ1-zWRW8s6CHKi6md5GWBdk0GupHr9Ml2KSXaEixIIJLC-7X1r6Wbwx4eQKxZpeKT6l-dbg1WCDlOrdiRlJl9j1NiqXo1PRhsY2awWX8hWcIaNy1Q8qVlgnEcGoLVHYYzniWE9mrV6rlSdQuyhplsf4xVha_7QlFE09BAJGrIeiFOOxE1p5ACI93TjIinZpHtELSoegKLVEHlEt5UHvwX39F-6wdbccAsdoK2jx_vheHYxuxYRNrwJksw9q3V4Q6chlEMr6dPJU7_pQ-bvPvXtSE5XFoOl3OVFiArGomEa4bIW1iBBkmoG1mJcvIlgDvcWor7nuT6_lPC48rFTQksLI3PJf-iyZWZP_psm2NeOfOuRNWHKoLxrdUDYVONOV6_0vMiqXPXsgLx9rC9SHdcq-OkDmJ1J3_09W1s8TVcPuqLGBY8tr3THPbWjA5G1qXKYJXLJnmnOZPfqhfEBpmCAxdDJZZG75Kg-1dDHyo0SX8oxIWA5wE-Y'
#     parent_code = "430a7a1288da4729907ae630c191db16"
#     file_path = "../france_soil_ph.tif"
#
#     # Optional progress callback
#     def progress_callback(current_chunk, total_chunks, percentage):
#         # You could update a progress bar here
#         pass
#
#     try:
#         uploader = FarmMapsUploader(token)
#         result = uploader.upload_file(file_path, parent_code, progress_callback)
#         print(f"🎉 Upload successful! File code: {result['code']}")
#
#     except Exception as e:
#         print(f"❌ Upload failed: {e}")
#
#
# if __name__ == "__main__":
#     main()
# import os
# import requests
# import time
# from typing import Optional
#
#
# class FarmMapsUploader:
#     def __init__(self, token: str):
#         self.token = token
#         self.base_url = "https://farmmaps.eu/api/v1/file"
#         self.chunk_size = 1048576  # 1MB
#
#     # def upload_file(self, file_path: str, parent_code: str, progress_callback: Optional[callable] = None) -> dict:
#     #     if not os.path.exists(file_path):
#     #         raise FileNotFoundError(f"❌ 文件未找到: {file_path}")
#     #
#     #     file_size = os.path.getsize(file_path)
#     #     file_name = os.path.basename(file_path)
#     #     print(f"📁 正在上传: {file_name} ({self._format_size(file_size)})")
#     #
#     #     # 注册文件
#     #     register_info = self._register_file(parent_code, file_name, file_size)
#     #
#     #     # 上传逻辑判断
#     #     if register_info["chunks"] == 1 and file_size <= 2 * 1024 * 1024:
#     #         self._upload_whole_file(file_path, register_info)
#     #     else:
#     #         self._upload_chunks(file_path, register_info, progress_callback)
#     #
#     #     print("✅ 文件上传完成！")
#     #     return register_info
#     def upload_file(self, file_path: str, parent_code: str, progress_callback: Optional[callable] = None) -> dict:
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"❌ 文件未找到: {file_path}")
#
#         file_size = os.path.getsize(file_path)
#         file_name = os.path.basename(file_path)
#         print(f"📁 正在上传: {file_name} ({self._format_size(file_size)})")
#
#         register_info = self._register_file(parent_code, file_name, file_size)
#
#         # ✅ 始终 chunk 上传，无论是1块还是多块
#         self._upload_chunks(file_path, register_info, progress_callback)
#
#         print("✅ 文件上传完成！")
#         return register_info
#
#     def _register_file(self, parent_code: str, file_name: str, file_size: int) -> dict:
#         payload = {
#             "parentCode": parent_code,
#             "name": file_name,
#             "size": file_size
#         }
#
#         # ✅ 仅大文件添加 chunkSize
#         if file_size > 2 * 1024 * 1024:
#             payload["chunkSize"] = self.chunk_size
#
#         headers = {
#             "Authorization": f"Bearer {self.token}",
#             "Content-Type": "application/json"
#         }
#
#         try:
#             response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
#             if response.status_code == 404 and "Parent not found" in response.text:
#                 raise ValueError("❌ parentCode 无效，请确认该文件夹是否存在，并且你有写入权限。")
#
#             response.raise_for_status()
#             register_info = response.json()
#
#             print(f"📝 注册成功，共分为 {register_info['chunks']} 个分块")
#             return register_info
#
#         except requests.exceptions.RequestException as e:
#             raise Exception(f"❌ 注册文件失败: {e}")
#     def _upload_whole_file(self, file_path: str, register_info: dict):
#         file_code = register_info['code']
#         upload_url = f"{self.base_url}/{file_code}"
#
#         headers = {
#             "Authorization": f"Bearer {self.token}",
#             "Content-Type": "application/octet-stream"
#         }
#
#         with open(file_path, 'rb') as f:
#             try:
#                 response = requests.post(upload_url, headers=headers, data=f, timeout=60)
#                 response.raise_for_status()
#                 print("📤 文件整体上传成功（小于2MB）")
#             except requests.exceptions.RequestException as e:
#                 raise Exception(f"❌ 整体上传失败: {e}")
#
#     def _upload_chunks(self, file_path: str, register_info: dict, progress_callback: Optional[callable] = None):
#         total_chunks = register_info['chunks']
#         chunk_size = register_info['chunkSize']
#         file_code = register_info['code']
#
#         # ✅ 正确的 header
#         headers = {
#             "Authorization": f"Bearer {self.token}",
#             "Content-Type": "application/octet-stream"
#         }
#
#         with open(file_path, 'rb') as f:
#             for chunk_number in range(1, total_chunks + 1):
#                 chunk_data = f.read(chunk_size)
#                 if not chunk_data:
#                     break
#
#                 success = False
#                 for attempt in range(3):
#                     try:
#                         # ✅ 注意中间的 /chunk/
#                         upload_url = f"{self.base_url}/{file_code}/chunk/{chunk_number}"
#                         response = requests.post(upload_url, headers={
#                             "Authorization": f"Bearer {self.token}",
#                             "Content-Type": "application/octet-stream"
#                         }, data=chunk_data, timeout=60)
#                         response.raise_for_status()
#                         success = True
#                         break
#                     except requests.exceptions.RequestException as e:
#                         if attempt < 2:
#                             print(f"⚠️ 第 {chunk_number} 块上传失败 (尝试 {attempt + 1})，重试中...")
#                             time.sleep(2 ** attempt)
#                         else:
#                             raise Exception(f"❌ 第 {chunk_number} 块上传失败: {e}")
#
#                 if success:
#                     progress = (chunk_number / total_chunks) * 100
#                     print(f"📦 块 {chunk_number}/{total_chunks} 上传成功 ({progress:.1f}%)")
#                     if progress_callback:
#                         progress_callback(chunk_number, total_chunks, progress)
#
#     @staticmethod
#     def _format_size(size_bytes: int) -> str:
#         for unit in ['B', 'KB', 'MB', 'GB']:
#             if size_bytes < 1024.0:
#                 return f"{size_bytes:.1f} {unit}"
#             size_bytes /= 1024.0
#         return f"{size_bytes:.1f} TB"
#
#
# def main():
#     # 🧠 替换为你自己的 token
#     token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkNERkM3M0I0NzY0Q0M5RTYxQTVDRjg3OEM5MDlFRUU0ODFFODk5MzFSUzI1NiIsIng1dCI6InpmeHp0SFpNeWVZYVhQaDR5UW51NUlIb21URSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZhcm1tYXBzLmV1IiwibmJmIjoxNzUwMTU3MzA4LCJpYXQiOjE3NTAxNTczMDgsImV4cCI6MTc1MDE2MDkwOCwiYXVkIjoiYXBpIiwic2NvcGUiOlsiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiZmFybW1hcHNfc3dhZ2dlciIsInN1YiI6ImI1MmRhMDhhOGE5YzRjNzlhYWVlMWU4ZDc2NTg3MTUwIiwiYXV0aF90aW1lIjoxNzQ5NjQ5MDk0LCJpZHAiOiJsb2NhbCIsInNpZCI6IkVGQ0IxMkQyNjU3RTc2NjQ4QTU3QjBFRUZDRDNFN0RGIiwiYXpwIjoiZmFybW1hcHNfc3dhZ2dlciIsImp0aSI6IjJCQTNERTM1QThDMUEzNEM0NkNBNDg5M0M2NTYwMjAxIn0.k-sdQuj99Vt9XCqdQFo1k4N6GE7YvsBx8FoT_ffcMceW3sbSZw2tDfX4ovP5IIYkjrlOJEbw9gcJJl0zDvm-mRUbKDZyrfrcPQzMAhY1AEsXYDwh8G7U3N_x5_T79L9l3aIUqX7RX4Ja-aXxHhYjoq9cn-s49ZW4UEFRIIq9jFIGN7Aqbj1AoPfKQSzgmoPKdxo3C8ojVfWrvv4AI9A3JjLtZam6_kmPMMdpKFvFFGqX69T0dn46fDmV-2HQ9yGcsEUnzQ89mNsBW7envP3kQhriNbxPTftjMgaNpSuY4Zdpngc4DJeMEaFQQDppE0EeU0iRoAGkz5Erln8ujYQNKmQQGNdvVUXBIqoo6v7PrdMqi5mF5Lc29uM2K6Xqxp7MVw58VzcxYYmo5DOVze8t_XQBL1dzIDF971tq7_4cXPFAkuAx8RkQ-U8PKLiLqwSSW6XP6kJLb52F6m7tIgt_FgAUqCwNBY8p89uXo8UQqbbSGEKe68Jb5FiPEH7zbZTxko6LFWgFO8Ojcp965fAbdnE3hqrH037mE6jBFju30FRAKgBPlmCEBI8UW80hdPOLkytGO5w1UGAd9QBSQ7wA3TT4BSTDXhY5JOZeajzRELeXeezBMuc4rw8P3huidq737OZDIGBAohcXI2RfPZVOXBcybIoUIirDrxebT-VQnCE'
#     # 🗂️ 替换为你在 FarmMaps 中拥有写入权限的 parent 文件夹 code
#     parent_code = "25ef92b2fa2745ef8271de9930b47fd6"
#
#     # 📄 替换为你本地的文件路径（建议用绝对路径）
#     file_path = "C:\D\projects\SoilDetection\SoilDetection\ireland_soil_pH.tif"
#
#     def progress_callback(current_chunk, total_chunks, percentage):
#         print(f"🔄 进度更新: {current_chunk}/{total_chunks} ({percentage:.1f}%)")
#
#     try:
#         uploader = FarmMapsUploader(token)
#         result = uploader.upload_file(file_path, parent_code, progress_callback)
#         print(f"🎉 上传成功！文件编码：{result['code']}")
#     except Exception as e:
#         print(str(e))
#
#
# if __name__ == "__main__":
#     main()
import os
import requests
import time
token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkNERkM3M0I0NzY0Q0M5RTYxQTVDRjg3OEM5MDlFRUU0ODFFODk5MzFSUzI1NiIsIng1dCI6InpmeHp0SFpNeWVZYVhQaDR5UW51NUlIb21URSIsInR5cCI6ImF0K2p3dCJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZhcm1tYXBzLmV1IiwibmJmIjoxNzUwMjYzNTQ5LCJpYXQiOjE3NTAyNjM1NDksImV4cCI6MTc1MDI2NzE0OSwiYXVkIjoiYXBpIiwic2NvcGUiOlsiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiZmFybW1hcHNfc3dhZ2dlciIsInN1YiI6ImI1MmRhMDhhOGE5YzRjNzlhYWVlMWU4ZDc2NTg3MTUwIiwiYXV0aF90aW1lIjoxNzQ5NjQ5MDk0LCJpZHAiOiJsb2NhbCIsInNpZCI6IkVGQ0IxMkQyNjU3RTc2NjQ4QTU3QjBFRUZDRDNFN0RGIiwiYXpwIjoiZmFybW1hcHNfc3dhZ2dlciIsImp0aSI6IkY4QTFFQkJEMjJBOTUyQUQzRTZEMzJEODU5NDJDOEM5In0.fOgmcZSiMYYdhsWrprBpduwpzFLnBPiVYeq7XY0YwoybL5fybQd-LnNy2QjqTUsKMDsedIaOncyEiguJD6UB8odiOeNeqaq97rSP4hM9Zvv9dID2GVMrxkzboy7LEIAIoKqzmIVIdqn0X86LZdtlgQiWvD-trn0yHE2cD5eyb0l4GfCvRwvuPhtUIJwmST2P6m6ajlurBMyRkAs_zxCaT35nMxUcK4E19v3-6zkveJxLJSKi93uMu7zkFvSrFoGh2Yo0mb60wDSwwfrOehDf9c4pxJDtgCIVMJlU4T55ubIjjFxM77b0DUMRUWJjhGeOKDOlzo0jlIjaAJwMIlPukIq5SE9RGugr1sdFQ2BfjAOOgS-GMku9Kl3kBKsGPfZPJKo0Vn8P5wsG7BgzwnOdDyA_79_83aaal5t56qslkv9n9c8PkJFHdyNMDQxGCJ_HodS44Aan2zVM3RP7jEIh8XPh1EXelzw1yOTI0Kkn3HB9pNeoQM15tEa9I3_pBoJhcCiltBUR72DOsd-QbZT9d84YeKd9139G4VSK6flWt1mMyjkdWm5rqX1O0gS5_s30oFtf7LOezPcItdgVhnLXgbxQgSlxpO2wAm_Y9xh4CwBoHzoNd1gGWuwl088FOz2qrOFNgg7G9xbakHCQFWT8LX8jqEJVaD_pUb9yECK9ddQ'
# file_path = "C:\D\projects\SoilDetection\SoilDetection\ireland_soil_pH.tif"
# file_path = "C:\D\projects\SoilDetection\SoilDetection\FarmmapAPI\\tifFile\\spain_soil_ph.tif"
file_path = r"C:\D\projects\SoilDetection\SoilDetection\FarmmapAPI\tifFile\spain_soil_ph.tif"
parent_code = "25ef92b2fa2745ef8271de9930b47fd6"

# Step 1: 注册文件
file_size = os.path.getsize(file_path)
file_name = os.path.basename(file_path)

reg_response = requests.post(
    "https://farmmaps.eu/api/v1/file",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "accept": "application/json"
    },
    json={
        "parentCode": parent_code,
        "name": file_name,
        "size": file_size
    }
)
reg_response.raise_for_status()
reg = reg_response.json()
file_code = reg["code"]
chunk_size = reg["chunkSize"]
print(reg)
print(f"register successfully，file_code: {file_code}, chunkSize: {chunk_size}")

# Step 2: Upload chunk
# file_path = "ireland_soil_pH.tif"
# file_code = "e6e9ec2e841740beaf1cbc97f8a4314e"  # 你从注册接口获取的
# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6..."  # 你的有效 Bearer token

upload_url = f"https://farmmaps.eu/api/v1/file/{file_code}/chunk/1"

headers = {
    "Authorization": f"Bearer {token}",
    "accept": "*/*"
}

# 模拟 multipart/form-data 文件上传
files = {
    'chunk': (file_path, open(file_path, 'rb'), 'image/tiff')
}

response = requests.post(upload_url, headers=headers, files=files)

print("✅ Status Code:", response.status_code)
print("📄 Response:", response.text)
response.raise_for_status()
# time.sleep(2)
# url = f"https://farmmaps.eu/api/v1/file/{file_code}"
# headers = {
#     "Authorization": f"Bearer {token}",
#     "Accept": "*/*"
# }
#
# response = requests.put(url, headers=headers)
# print("✅ 确认上传状态码:", response.status_code)
# print("📄 返回信息:", response.text)

# url = f"https://farmmaps.eu/api/v1/file/{file_code}"
# headers = {
#     "Authorization": f"Bearer {token}",
#     "accept": "*/*"
# }
#
# # 发送 DELETE 请求
# response = requests.delete(url, headers=headers)
#
# # 输出结果
# print("✅ 状态码:", response.status_code)
# print("📄 返回信息:", response.text)