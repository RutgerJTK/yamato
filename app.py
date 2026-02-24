import streamlit as st

PASSWORD = "zimone"


def login_page():
    st.title("Yatamato")
    st.subheader("Please log in to continue")

    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        if password == PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")


def front_page():
    st.title("Yatamato")
    st.subheader("Welcome to Yatamato – your simple task tracker")

    st.markdown(
        """
        Yatamato helps you create and manage small stories and tasks,
        much like Jira or Asana, but way more bare-bones.

        **Get started** by using the sidebar to navigate through the app.
        """
    )

    if st.button("Log out"):
        st.session_state["authenticated"] = False
        st.rerun()


def main():
    st.set_page_config(page_title="Yatamato", page_icon="✅")

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        front_page()
    else:
        login_page()


if __name__ == "__main__":
    main()
