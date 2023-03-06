try:

    from enum import Enum
    from io import BytesIO, StringIO
    from typing import Union
    import os

    import pandas as pd
    import streamlit as st
except Exception as e:
    print(e)

STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

UPLOAD_DIRECTORY = "uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


class FileUpload(object):

    def __init__(self):
        self.fileTypes = ["csv", "png", "jpg", "jpeg", "mp4", "webm", "ogg"]

    def save_file(self, file):
        file_path = os.path.join(UPLOAD_DIRECTORY, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        return file_path

    def run(self):
        """
        Upload File on Streamlit Code
        :return:
        """
        st.info(__doc__)
        st.markdown(STYLE, unsafe_allow_html=True)
        files = st.file_uploader("Upload files", type=self.fileTypes, accept_multiple_files=True)
        if not files:
            st.warning("Please upload a file of type: " + ", ".join(self.fileTypes))
            return
        selected_files = []
        for file in files:
            content = file.getvalue()
            if file.type.startswith('image/'):
                st.image(file, use_column_width=True)
            elif file.type.startswith('video/'):
                st.video(file)
            elif file.type == 'text/csv':
                data = pd.read_csv(file)
                st.dataframe(data.head(10))
            else:
                st.warning("Unsupported file type: " + file.type)
                continue
            if st.checkbox("Save " + file.name):
                file_path = self.save_file(file)
                selected_files.append(file_path)
        if selected_files:
            st.success("Saved files:")
            for file_path in selected_files:
                st.write(file_path)
                file_name = os.path.basename(file_path)
                mime_type = "auto"
                if file_name.endswith(".csv"):
                    mime_type = "text/csv"
                elif file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
                    mime_type = "image/jpeg"
                elif file_name.endswith(".png"):
                    mime_type = "image/png"
                elif file_name.endswith(".mp4"):
                    mime_type = "video/mp4"
                elif file_name.endswith(".webm"):
                    mime_type = "video/webm"
                elif file_name.endswith(".ogg"):
                    mime_type = "audio/ogg"
                st.download_button(
                    label="Download " + file_name,
                    data=open(file_path, "rb").read(),
                    file_name=file_name,
                    mime=mime_type
                )


if __name__ == "__main__":
    helper = FileUpload()
    helper.run()


