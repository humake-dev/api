# config valid for current version and patch releases of Capistrano
lock "~> 3.19.2"

set :application, "humake_API"
set :repo_url, "git@github.com:humake-dev/api.git"

# Default branch is :master
set :branch, "main"

# Default deploy_to directory is /var/www/my_app_name
set :deploy_to, "/var/www/vhosts/api"

# Default value for :format is :airbrussh.
# set :format, :airbrussh

# You can configure the Airbrussh format using :format_options.
# These are the defaults.
# set :format_options, command_output: true, log_file: "log/capistrano.log", color: :auto, truncate: :auto

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
append :linked_files, ".env"

# Default value for linked_dirs is []
append :linked_dirs, "log", "static"

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for local_user is ENV['USER']
# set :local_user, -> { `git config user.name`.chomp }

# Default value for keep_releases is 5
set :keep_releases, 3

set :default_env, {
  PATH: "$HOME/.local/bin:$PATH"
}

namespace :deploy do
  desc "Restart API service"
  task :restart_api do
    on roles(:app) do
      execute :sudo, :systemctl, :restart, :humake_api
    end
  end
end

# Uncomment the following to require manually verifying the host key before first deploy.
# set :ssh_options, verify_host_key: :secure
after 'deploy:updated', 'poetry:install'
#after "deploy:published", "deploy:restart_api"